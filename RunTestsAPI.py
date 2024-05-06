import pytest, os, argparse

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Swagger API test tool", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e", "--env", help="API environment")
parser.add_argument("-ap", "--api_provider", help="API provider")
args = parser.parse_args()
config = vars(args)

azure_prod_api_url = "https://api.connectlife.io"
azure_test_api_url = "https://api-test.connectlife.io"
aws_test_api_url = "https://dnejtsakgzwih.cloudfront.net"

api_url = azure_test_api_url
env = config["env"]
if config["api_provider"] == "aws":
    api_url = aws_test_api_url
elif config["api_provider"] == "azure":
    if env == "prod":
        api_url = azure_prod_api_url
    else:
        api_url = azure_test_api_url

def pre_tests() -> int:
    # order is important
    retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetWizardsAll"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetRecipesIdLang"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetRecipesPagedDetailLang"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetRecipesPagedLang"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetConnectivityGroupsProductCodes"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetAppliances"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetProductsAuids"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "PutApplianceApplianceProfileAfota"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetApplianceApplianceProfileAuids"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "PutApplianceApplianceProfileHeidi"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "GetApplianceApplianceProfileMultiAuids"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "PreTests", "Content"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])

    return retcode

def main() -> int:
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "Appliance"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "Content"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "Manuals"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "Products"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "Recipe"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "WashingPrograms"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(ROOT_DIR, "WebAPI", "ConnectLife", "Tests", "Wizards"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    
    # # retcode = pytest.main(["WebAPI/HiJuConn/Tests/", "-s", "--auth", "juconnect"])
    # return retcode
    pass

# mode = [all, empty]
def clean_error_logs(mode="all"):
    try:
        for root, subfiles, files in os.walk(os.path.join(ROOT_DIR, "report_logs")):
            for f in files:
                if "_logs_" in f:
                    filePath = os.path.join(root, f)

                    if mode == "all":
                        if os.path.isfile(filePath):
                            os.remove(filePath)
                            print(f"Deleted: {filePath}")
                    elif mode == "empty":
                        opened_file = open(filePath, "r")
                        lines = opened_file.readlines()
                        opened_file.close()
                        if len(lines) <= 1:
                            if os.path.isfile(filePath):
                                os.remove(filePath)
                                print(f"Deleted: {filePath}")
    except Exception as ex:
        if hasattr(ex, 'message'):
            print(ex.message)
        else:
            print(ex)

if __name__ == "__main__":
    clean_error_logs("all")
    pre_tests()
    main()
    clean_error_logs("empty")
