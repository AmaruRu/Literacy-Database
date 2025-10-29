#!/usr/bin/env python3
"""
Database Health Monitoring Script for Mississippi Literacy Database
Lightweight daily health checks and alerting
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import create_website, db
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

def run_health_check():
    """Run lightweight database health check"""
    health_status = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'checks': [],
        'alerts': []
    }
    
    try:
        app = create_website()
        
        with app.app_context():
            # Check 1: Database connectivity
            try:
                count = db.session.execute(db.text("SELECT 1")).scalar()
                health_status['checks'].append({
                    'name': 'database_connectivity',
                    'status': 'pass',
                    'message': 'Database connection successful'
                })
            except Exception as e:
                health_status['checks'].append({
                    'name': 'database_connectivity',
                    'status': 'fail',
                    'message': f'Database connection failed: {e}'
                })
                health_status['status'] = 'critical'
                return health_status
            
            # Check 2: Record counts (detect major data loss)
            expected_counts = {
                'Districts': 147,
                'Schools': 853,
                'Subgroups': 29,
                'Performance_Data': 19377
            }
            
            for table, expected in expected_counts.items():
                try:
                    actual = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    variance = abs(actual - expected) / expected * 100
                    
                    if variance > 10:  # More than 10% variance
                        health_status['checks'].append({
                            'name': f'{table}_count',
                            'status': 'warning',
                            'message': f'{table}: {actual} records (expected ~{expected}, {variance:.1f}% variance)'
                        })
                        health_status['alerts'].append(f'Record count variance in {table}: {variance:.1f}%')
                        if health_status['status'] == 'healthy':
                            health_status['status'] = 'warning'
                    else:
                        health_status['checks'].append({
                            'name': f'{table}_count',
                            'status': 'pass',
                            'message': f'{table}: {actual} records (healthy)'
                        })
                        
                except Exception as e:
                    health_status['checks'].append({
                        'name': f'{table}_count',
                        'status': 'fail',
                        'message': f'Failed to count {table}: {e}'
                    })
                    health_status['status'] = 'critical'
            
            # Check 3: Data quality flags
            try:
                flagged_records = db.session.execute(db.text('''
                    SELECT COUNT(*) FROM Performance_Data 
                    WHERE Data_Quality_Flags IS NOT NULL
                ''')).scalar()
                
                health_status['checks'].append({
                    'name': 'data_quality_flags',
                    'status': 'info',
                    'message': f'{flagged_records:,} records with quality flags'
                })
                
            except Exception as e:
                health_status['checks'].append({
                    'name': 'data_quality_flags',
                    'status': 'warning',
                    'message': f'Could not check quality flags: {e}'
                })
            
            # Check 4: Recent activity (if timestamps exist)
            try:
                recent_updates = db.session.execute(db.text('''
                    SELECT COUNT(*) FROM Performance_Data 
                    WHERE Updated_At > DATE_SUB(NOW(), INTERVAL 7 DAY)
                ''')).scalar()
                
                health_status['checks'].append({
                    'name': 'recent_activity',
                    'status': 'info',
                    'message': f'{recent_updates} records updated in last 7 days'
                })
                
            except Exception as e:
                # Column might not exist, skip this check
                pass
                
    except Exception as e:
        health_status['status'] = 'critical'
        health_status['alerts'].append(f'Health check failed: {e}')
    
    return health_status

def print_health_report(health_status):
    """Print formatted health report"""
    status_emoji = {
        'healthy': '🟢',
        'warning': '🟡', 
        'critical': '🔴'
    }
    
    print(f"\n{status_emoji.get(health_status['status'], '❓')} Database Health Status: {health_status['status'].upper()}")
    print(f"🕐 Check time: {health_status['timestamp']}")
    
    if health_status['alerts']:
        print(f"\n🚨 Alerts ({len(health_status['alerts'])}):")
        for alert in health_status['alerts']:
            print(f"  - {alert}")
    
    print(f"\n📋 Health Checks ({len(health_status['checks'])}):")
    for check in health_status['checks']:
        status_symbol = {'pass': '✅', 'warning': '⚠️', 'fail': '❌', 'info': 'ℹ️'}.get(check['status'], '❓')
        print(f"  {status_symbol} {check['name']}: {check['message']}")
    
    return health_status['status'] == 'healthy'

def save_health_log(health_status):
    """Save health check to log file"""
    log_file = '/Users/kershadwooten/Desktop/Literacy-Database/dev/health_log.jsonl'
    
    try:
        with open(log_file, 'a') as f:
            f.write(json.dumps(health_status) + '\n')
    except Exception as e:
        print(f"⚠️ Could not save health log: {e}")

def main():
    """Main health check function"""
    print("🔍 Running Database Health Check...")
    
    health_status = run_health_check()
    is_healthy = print_health_report(health_status)
    save_health_log(health_status)
    
    if is_healthy:
        print("\n✅ Health check completed - All systems normal")
        exit(0)
    elif health_status['status'] == 'warning':
        print("\n⚠️ Health check completed - Warnings detected")
        exit(1)
    else:
        print("\n❌ Health check completed - Critical issues detected")
        exit(2)

if __name__ == "__main__":
    main()