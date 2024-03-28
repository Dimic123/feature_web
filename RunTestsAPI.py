import pytest, os

currentDirectory = os.path.dirname(os.path.realpath(__file__))

# api_url = "https://api.connectlife.io"
# api_url = "https://api-test.connectlife.io"
api_url = "https://dnejtsakgzwih.cloudfront.net"

# env = "prod"
env = "test"

def pre_tests() -> int:
    # ordering is important!

    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetWizardsAll", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetRecipesIdLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetRecipesPagedDetailLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetRecipesPagedLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetConnectivityGroupsProductCodes", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetAppliances", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\GetProductsAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\PutApplianceApplianceProfileAfota", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])   

    retcode = pytest.main([f".\WebAPI\ConnectLife\PreTests\Content", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Manuals\\1_GetManualsAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])

    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\1_GetFaqsAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url]) ## SLOWS DOWN
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\2_GetFaqsAuidsLangs", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\3_GetTipsTricksAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url]) ## SLOWS DOWN
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\4_GetTipsTricksAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\5_GetInspirationsAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\6_GetInspirationsAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    ## retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\6_GetInspirationsAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\7_GetPairingAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\8_GetPairingAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\9_GetPairingWifiAuids", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\10_GetPairingWifiAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\11_GetHelp", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\12_GetHelpLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\13_GetHelpAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\14_GetGenericFaq", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\15_GetGenericFaqLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\16_GetGenericFaqAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\17_GetGuides", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\18_GetGuidesLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content\\19_GetGuidesAuidsLang", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])

    return retcode

def main() -> int:
    # retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Products\\1_GetProductsAuids", "-s", "--auth", "cdc", "--env", "test", "--apiBaseUrl", api_url])

    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Appliance", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Content", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Manuals", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Products", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Recipe", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\WashingPrograms", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])
    retcode = pytest.main([f".\WebAPI\ConnectLife\Tests\Wizards", "-s", "--auth", "cdc", "--env", env, "--apiBaseUrl", api_url])

    # retcode = pytest.main(["WebAPI/HiJuConn/Tests/", "-s", "--auth", "juconnect"])
    return retcode

def clear_report_logs():
    try:
        for root, files in os.walk(os.path.join(currentDirectory, "report_logs")):
            for f in files:
                if "_logs_" in f:
                    filePath = os.path.join(root, f)
                    if os.path.isfile(filePath):
                        os.remove(filePath)
                        print(f"Deleted: {filePath}")
    except Exception as ex:
        if hasattr(ex, 'message'):
            print(ex.message)
        else:
            print(ex)
            

def remove_empty_logs():
    try:
        for root, files in os.walk(os.path.join(currentDirectory, "report_logs")):
            for f in files:
                filePath = os.path.join(root, f)

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
    clear_report_logs()
    pre_tests()
    # main()
    remove_empty_logs()
