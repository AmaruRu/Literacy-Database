#!/usr/bin/env python3
"""
Test script for API endpoints
"""

import json
from project import create_website

def test_api_endpoints():
    """Test API endpoints"""
    
    # Create Flask app
    app = create_website()
    
    with app.test_client() as client:
        print("Testing API Endpoints...")
        print("=" * 50)
        
        # Test health check
        print("1. Testing Health Check...")
        response = client.get('/api/health')
        data = response.get_json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ Health check passed - {data['district_count']} districts in database")
        else:
            print(f"   ❌ Health check failed: {data}")
        
        # Test get districts
        print("\n2. Testing Get Districts...")
        response = client.get('/api/districts')
        data = response.get_json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ Retrieved {data['count']} districts")
            if data['data']:
                sample = data['data'][0]
                print(f"   Sample: {sample['district_name']} ({sample['school_count']} schools)")
        else:
            print(f"   ❌ Get districts failed: {data}")
        
        # Test district detail
        print("\n3. Testing District Detail...")
        if data.get('data') and len(data['data']) > 0:
            district_id = data['data'][0]['district_id']
            response = client.get(f'/api/districts/{district_id}')
            detail_data = response.get_json()
            
            if response.status_code == 200 and detail_data.get('success'):
                district = detail_data['data']
                print(f"   ✅ District details for '{district['district_name']}'")
                print(f"   Schools: {len(district['schools'])}")
                if district['performance_summary']:
                    prof = district['performance_summary']['english_proficiency']
                    print(f"   English Proficiency: {prof}%")
            else:
                print(f"   ❌ District detail failed: {detail_data}")
        
        # Test get subgroups
        print("\n4. Testing Get Subgroups...")
        response = client.get('/api/subgroups')
        data = response.get_json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ Retrieved {data['count']} subgroups")
            categories = {}
            for sg in data['data']:
                cat = sg['subgroup_category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for category, count in categories.items():
                print(f"   {category}: {count} subgroups")
        else:
            print(f"   ❌ Get subgroups failed: {data}")
        
        # Test performance data
        print("\n5. Testing Performance Data...")
        response = client.get('/api/performance?limit=5&subgroup_id=1')  # 'All' subgroup
        data = response.get_json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ Retrieved {data['count']} performance records")
            if data['data']:
                sample = data['data'][0]
                print(f"   Sample: {sample['district_name']} - {sample['subgroup_name']}")
                print(f"   English Proficiency: {sample['english_proficiency']}%")
        else:
            print(f"   ❌ Performance data failed: {data}")
        
        # Test district rankings
        print("\n6. Testing District Rankings...")
        response = client.get('/api/analytics/district-rankings')
        data = response.get_json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ Retrieved rankings for {data['count']} districts")
            print("   Top 3 Districts:")
            for district in data['data'][:3]:
                print(f"   {district['rank']}. {district['district_name']}: {district['average_english_proficiency']}%")
        else:
            print(f"   ❌ District rankings failed: {data}")
        
        # Test subgroup performance
        print("\n7. Testing Subgroup Performance Analysis...")
        response = client.get('/api/analytics/subgroup-performance')
        data = response.get_json()
        
        if response.status_code == 200 and data.get('success'):
            print(f"   ✅ Retrieved performance for {data['count']} subgroups")
            
            # Group by category
            by_category = {}
            for sg in data['data']:
                cat = sg['subgroup_category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(sg)
            
            for category, subgroups in by_category.items():
                print(f"   {category} Category:")
                for sg in subgroups[:3]:  # Show top 3 in each category
                    prof = sg['average_english_proficiency']
                    print(f"     - {sg['subgroup_name']}: {prof}%")
        else:
            print(f"   ❌ Subgroup performance failed: {data}")
        
        print(f"\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api_endpoints()