import scrapy


class MlSpider(scrapy.Spider):
    name = 'ml'
    
    start_urls = ['https://www.mercadolivre.com.br/ofertas#nav-header']

    def parse(self, response):
        #Pega o link de todos os authores
        author_page_links = response.css('.promotion-item__link-container::attr(href)')
        yield from response.follow_all(author_page_links, self.parse_author)
        
        
        #Pega todos os links das proximas paginas
        pagination_links = response.css('a.andes-pagination__link::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)


    #Funcao que extrai os dados das paginas
    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        #Armazena os dados em dicionario   
        yield {
            'name': extract_with_css('h1.ui-pdp-title::text'),
            'preco': extract_with_css('span.andes-money-amount__fraction::text'),
            'avaliacao': extract_with_css('span.ui-pdp-review__amount::text'),
        }
