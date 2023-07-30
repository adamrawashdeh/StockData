from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import xml.dom.minidom as minidom

app = Flask(__name__)


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def perform_search():
    stock_symbol = request.args.get('symbol')
    if stock_symbol:
        os.system(f"./stock.sh {stock_symbol}")
        return redirect(url_for('index', symbol=stock_symbol))
    return render_template('search.html', message="Please provide a stock symbol.")

@app.route('/stock')
def index():
    stock_symbol = request.args.get('symbol')
    if stock_symbol:
        xml_file = f"{stock_symbol}.xhtml"
        domtree = minidom.parse(xml_file)
        group = domtree.documentElement
        divs = group.getElementsByTagName('div')
        h1s = group.getElementsByTagName('h1')
        ranges = group.getElementsByTagName('mw-rangeBar')

        StockName = ''
        StockSymbol = ''
        StockPrice = ''
        StockDescription = ''
        OpenPrice = ''
        ClosePrice = ''
        MarketCap = ''
        Float = ''
        PriceEarnings_Ratio = ''
        YearLow = ''
        YearHigh = ''
        DayLow = ''
        DayHigh = ''
        Volume = ''
        AverageVolume = ''


        for h1 in h1s:
            if h1.getAttribute('class') == 'company__name':
                StockName = h1.firstChild.nodeValue

        for range in ranges:
            if range.getAttribute('class') == 'element element--range range--yearly':
                spans = range.getElementsByTagName('span')
                YearLow = spans[0].firstChild.nodeValue
                YearHigh = spans[2].firstChild.nodeValue

            if range.getAttribute('class') == 'element element--range range--daily':
                spans = range.getElementsByTagName('span')
                DayLow = spans[0].firstChild.nodeValue
                DayHigh = spans[2].firstChild.nodeValue
            
            if range.getAttribute('class') == 'element element--range range--volume':
                spans = range.getElementsByTagName('span')
                for span in spans:
                    if span.getAttribute('class') == 'primary':
                        Volume = span.firstChild.nodeValue


        for div in divs:
            if div.getAttribute('class') == 'intraday__close':
                closes = div.getElementsByTagName('td')
                for close in closes:
                    if close.getAttribute('class') == 'table__cell u-semi':
                        ClosePrice = close.firstChild.nodeValue

            if div.getAttribute('class') == 'element element--description description__long':
                descriptions = div.getElementsByTagName('p')
                for description in descriptions:
                    if description.getAttribute('class') == 'description__text':
                        StockDescription = description.firstChild.nodeValue

            if div.getAttribute('class') == 'element element--list':
                stats = div.getElementsByTagName('li')
                for stat in stats:
                    label = stat.getElementsByTagName('small')[0].firstChild.nodeValue
                    if label == 'Open':
                        OpenPrice = stat.getElementsByTagName('span')[0].firstChild.nodeValue
                    if label == 'Market Cap':
                        MarketCap = stat.getElementsByTagName('span')[0].firstChild.nodeValue
                    if label == 'Public Float':
                        Float = stat.getElementsByTagName('span')[0].firstChild.nodeValue
                    if label == 'P/E Ratio':
                        PriceEarnings_Ratio = stat.getElementsByTagName('span')[0].firstChild.nodeValue
                    if label == 'Average Volume':
                        AverageVolume = stat.getElementsByTagName('span')[0].firstChild.nodeValue

            if div.getAttribute('class') == 'element element--intraday':
                prices = div.getElementsByTagName('bg-quote')
                names = div.getElementsByTagName('span')

                for price in prices:
                    if price.getAttribute('class') == 'value':
                        StockPrice = price.firstChild.nodeValue

                for name in names:
                    if name.getAttribute('class') == 'company__ticker':
                        StockSymbol = name.firstChild.nodeValue


        return render_template('index.html', StockName=StockName, StockSymbol=StockSymbol, StockPrice=StockPrice, StockDescription=StockDescription, OpenPrice=OpenPrice, ClosePrice=ClosePrice, MarketCap=MarketCap, Float=Float, PriceEarnings_Ratio=PriceEarnings_Ratio, YearLow=YearLow, YearHigh=YearHigh, DayLow=DayLow, DayHigh=DayHigh, Volume=Volume, AverageVolume=AverageVolume)
    return "No stock symbol provided."

if __name__ == '__main__':
    app.run()