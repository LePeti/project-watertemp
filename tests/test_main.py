from mock import patch

from src.main import get_watertemp_page


class TestScraping:
    @patch("src.main.requests.get")
    def test_get_watertemp_page_correctURLPassed(self, mock_get_request):
        get_watertemp_page()
        assert (
            mock_get_request.call_args_list[0][0][0]
            == "https://www.eumet.hu/vizhomerseklet/"
        )
