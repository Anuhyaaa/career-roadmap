"""
API Test Script - Test all Career Roadmap Generator endpoints
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n🔍 Testing user registration...")
    try:
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 201:
            print("✅ User registration passed")
            result = response.json()
            print(f"   User created: {result['user']['email']}")
            return True, response.cookies
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return False, None

def test_user_login():
    """Test user login"""
    print("\n🔍 Testing user login...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login passed")
            result = response.json()
            print(f"   Logged in user: {result['user']['email']}")
            return True, response.cookies
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return False, None

def test_roadmap_generation(cookies=None):
    """Test roadmap generation"""
    print("\n🔍 Testing roadmap generation...")
    try:
        roadmap_data = {
            "interests": "web development, javascript, react",
            "education": "bachelors",
            "currentSkills": "HTML, CSS, basic JavaScript",
            "careerGoal": "Full-stack developer"
        }
        response = requests.post(f"{BASE_URL}/api/generate-roadmap", json=roadmap_data, cookies=cookies)
        if response.status_code == 200:
            print("✅ Roadmap generation passed")
            result = response.json()
            print(f"   Generated roadmap ID: {result['roadmap_id']}")
            print(f"   Skills in path: {len(result['roadmap']['skill_path'])}")
            return True, result['roadmap_id']
        else:
            print(f"❌ Roadmap generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ Roadmap generation error: {e}")
        return False, None

def test_roadmap_retrieval(roadmap_id, cookies=None):
    """Test roadmap retrieval"""
    print("\n🔍 Testing roadmap retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/roadmaps/{roadmap_id}", cookies=cookies)
        if response.status_code == 200:
            print("✅ Roadmap retrieval passed")
            result = response.json()
            print(f"   Retrieved roadmap: {result['id']}")
            return True
        else:
            print(f"❌ Roadmap retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Roadmap retrieval error: {e}")
        return False

def test_roadmap_history(cookies=None):
    """Test roadmap history"""
    print("\n🔍 Testing roadmap history...")
    try:
        response = requests.get(f"{BASE_URL}/api/roadmaps/history", cookies=cookies)
        if response.status_code == 200:
            print("✅ Roadmap history passed")
            result = response.json()
            print(f"   Found {len(result['roadmaps'])} roadmaps in history")
            return True
        else:
            print(f"❌ Roadmap history failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Roadmap history error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API Tests for Career Roadmap Generator")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Basic health check failed. Server might not be running.")
        sys.exit(1)
    
    # Test user registration
    reg_success, reg_cookies = test_user_registration()
    
    # Test user login  
    login_success, login_cookies = test_user_login()
    cookies = login_cookies if login_success else reg_cookies
    
    # Test roadmap generation
    roadmap_success, roadmap_id = test_roadmap_generation(cookies)
    
    # Test roadmap retrieval
    if roadmap_success and roadmap_id:
        test_roadmap_retrieval(roadmap_id, cookies)
    
    # Test roadmap history
    if login_success or reg_success:
        test_roadmap_history(cookies)
    
    print("\n" + "=" * 60)
    print("🎉 API testing completed!")
    print("\n💡 Next steps:")
    print("   1. Update frontend to use these API endpoints")
    print("   2. Test integration with the React frontend") 
    print("   3. Add MongoDB integration for production")
    print("   4. Implement PDF export functionality")

if __name__ == "__main__":
    main()