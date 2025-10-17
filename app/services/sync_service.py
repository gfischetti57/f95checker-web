import sqlite3
import re
import os
from datetime import datetime
from flask import current_app
from app import db
from app.models.game import Game

class SyncService:
    
    @staticmethod
    def sync_threads_from_desktop():
        """Sincronizza thread dal database desktop F95Checker al web"""
        desktop_db_path = current_app.config.get('DESKTOP_DB_PATH')
        
        if os.path.exists(desktop_db_path):
            return SyncService._sync_from_desktop_db(desktop_db_path)
        else:
            return SyncService._sync_from_hardcoded_list()
    
    @staticmethod
    def _sync_from_desktop_db(db_path):
        """Sincronizza dal database desktop"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, url, version, developer 
                FROM games 
                WHERE url LIKE '%f95zone.to/threads/%'
            """)
            
            desktop_games = cursor.fetchall()
            conn.close()
            
            existing_threads = set(game.f95_id for game in Game.query.all())
            added_count = 0
            updated_count = 0
            
            for name, url, version, developer in desktop_games:
                match = re.search(r'f95zone\.to/threads/(\d+)', url)
                if not match:
                    continue
                    
                thread_id = match.group(1)
                existing_game = Game.query.filter_by(f95_id=thread_id).first()
                
                if existing_game:
                    if existing_game.version != version:
                        existing_game.version = version
                        existing_game.title = name
                        existing_game.last_updated = datetime.utcnow()
                        updated_count += 1
                else:
                    new_game = Game(
                        f95_id=thread_id,
                        title=name,
                        url=url,
                        version=version,
                        last_updated=datetime.utcnow(),
                        last_checked=datetime.utcnow(),
                        is_active=True
                    )
                    db.session.add(new_game)
                    added_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'added': added_count,
                'updated': updated_count,
                'total_desktop': len(desktop_games),
                'total_web': Game.query.count(),
                'source': 'desktop_db'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def _sync_from_hardcoded_list():
        """Fallback con lista hardcoded"""
        thread_ids = [
            '4815', '4907', '9201', '9414', '10549', '12181', '12760', '14509', '15459', '15780',
            '18418', '19856', '20072', '25081', '25264', '25332', '28008', '29627', '29666', '29981',
            '31351', '33424', '33607', '33740', '33797', '35068', '35910', '36240', '37470', '38131',
            '41188', '42509', '42668', '45466', '45993', '46344', '46615', '48734', '48813', '49572',
            '50281', '50772', '50840', '51634', '52621', '53676', '54521', '55785', '56110', '62625',
            '63437', '65913', '65957', '67104', '67494', '68105', '69272', '70133', '70546', '71348',
            '72109', '72480', '74436', '75232', '77680', '79512', '79740', '80371', '80788', '85108',
            '85276', '85280', '85755', '87506', '88718', '90433', '93340', '94140', '95142', '97784',
            '98717', '99976', '102771', '106028', '106180', '107102', '112027', '112212', '112700',
            '115549', '115722', '119199', '120317', '122582', '125509', '126219', '129541', '129788',
            '130096', '133017', '134764', '135123', '137720', '140205', '140284', '140310', '141186',
            '142322', '142460', '143045', '143132', '143711', '144318', '145408', '151505', '154475',
            '154533', '155304', '156149', '156308', '158858', '159512', '160139', '160909', '160994',
            '165755', '166735', '167178', '171221', '177547', '182094', '183721', '183779', '184252',
            '184552', '188848', '193794', '197127', '200080', '214365', '215260', '219307', '224938',
            '229269', '230209', '230968', '237702', '238093', '238419', '241164', '270027', '270418',
            '270962', '271592'
        ]
        
        try:
            existing_threads = set(game.f95_id for game in Game.query.all())
            added_count = 0
            
            for thread_id in thread_ids:
                if thread_id not in existing_threads:
                    new_game = Game(
                        f95_id=thread_id,
                        title=f'Thread {thread_id}',
                        url=f'https://f95zone.to/threads/{thread_id}',
                        last_updated=datetime.utcnow(),
                        last_checked=datetime.utcnow(),
                        is_active=True
                    )
                    db.session.add(new_game)
                    added_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'added': added_count,
                'updated': 0,
                'total_desktop': len(thread_ids),
                'total_web': Game.query.count(),
                'source': 'hardcoded_list'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }