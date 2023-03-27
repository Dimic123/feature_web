from WebAPI.Swagger.Common.Authorization import *
from WebAPI.Swagger.Tests.GetAppliances import *
from WebAPI.Swagger.Tests.GetApplianceProperties import *

def main():
	TestAPI()

def TestAPI():
    # Auth, get token
    token = AuthAPI("test5@connectlife.io","LJijveUqxQNv3T27RSnhOgkhThYeZYt++WvWgc37ThwNUPziKgVgPMak7oujF2fIOcdiGjQVUMjdYghd9Qj8hA==","5065059336212","07swfKgvJhC3ydOUS9YV_SwVz0i4LKqlOLGNUukYHVMsJRF1b-iWeUGcNlXyYCeK")
    if token is None:
        print("ERROR - token was not retrieved, canceling tests")
        return False
    
    # Tests
    GetAppliances(token)
    GetApplianceProperty(token, "8650021000100020002000000d2ffa0d0680-0000000000007389860001202100012030002")
    
    return True

if __name__ == "__main__":
	main()