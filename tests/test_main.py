from mock import patch

from src.main import get_watertemp_page
from src.main import scrape_watertemp_tables


class TestScraping:
    @patch("src.main.requests.get")
    def test_get_watertemp_page_correctURLPassed(self, mock_get_request):
        get_watertemp_page()
        assert (
            mock_get_request.call_args_list[0][0][0]
            == "https://www.eumet.hu/vizhomerseklet/"
        )

    @patch("src.main.pd.read_html")
    def test_scrape_watertemp_tables_correctURLPassed(self, mock_read_html):
        scrape_watertemp_tables()
        assert (
            mock_read_html.call_args_list[0][0][0]
            == "https://www.eumet.hu/vizhomerseklet/"
        )
