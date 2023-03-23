from WebAPI.Swagger.Common.Authorization import *
from WebAPI.Swagger.Tests.GetAppliances import GetAppliances

def main():
	TestAPI()

def TestAPI():
    token = AuthAPI("test5@connectlife.io","LJijveUqxQNv3T27RSnhOgkhThYeZYt++WvWgc37ThwNUPziKgVgPMak7oujF2fIOcdiGjQVUMjdYghd9Qj8hA==","5065059336212","07swfKgvJhC3ydOUS9YV_SwVz0i4LKqlOLGNUukYHVMsJRF1b-iWeUGcNlXyYCeK")
    GetAppliances(token)

if __name__ == "__main__":
	main()