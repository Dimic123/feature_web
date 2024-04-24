import pytest, os

currentDirectory = os.path.dirname(os.path.realpath(__file__))

azure_prod_api_url = "https://api.connectlife.io"
azure_test_api_url = "https://api-test.connectlife.io"
aws_test_api_url = "https://dnejtsakgzwih.cloudfront.net"

env = "test"
api_url = azure_test_api_url

if api_url == aws_test_api_url or api_url == azure_test_api_url:
    env = "test"
elif api_url == azure_prod_api_url:
    env == "prod"

def pre_tests() -> int:
    # order is important
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetWizardsAll"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetRecipesIdLang"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetRecipesPagedDetailLang"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetRecipesPagedLang"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetConnectivityGroupsProductCodes"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetAppliances"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetProductsAuids"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\PutApplianceApplianceProfileAfota"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\Content"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\GetAppliancesApplianceProfileAuids"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\PreTests\PutApplianceApplianceProfileHeidi"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])

    return retcode

def main() -> int:
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\1_GetFaqsAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\Tests\Wizards\\6_PostWizardStoringfoodMultipleWizardId"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([os.path.join(currentDirectory, "WebAPI\ConnectLife\Tests\Wizards\\6_PostWizardStoringfoodMultipleWizardId"), "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Appliance\\12_GetAppliancesApplianceProfileAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Appliance", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Manuals", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Products", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Recipe", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\WashingPrograms", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Wizards", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    
    # retcode = pytest.main(["WebAPI/HiJuConn/Tests/", "-s", "--auth", "juconnect"])
    return retcode

# mode = [all, empty]
def clean_error_logs(mode="all"):
    try:
        for root, subfiles, files in os.walk(os.path.join(currentDirectory, "report_logs")):
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
    # pre_tests()
    main()
    clean_error_logs("empty")
