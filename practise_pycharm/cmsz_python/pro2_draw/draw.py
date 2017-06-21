# -*- encoding: utf-8 -*-

from reportlab.graphics.charts.lineplots import *
from reportlab.graphics.charts.textlabels import *
from reportlab.graphics import renderPDF

"""
URL = 'http://www.SWPC.noaa.gov/ftpdir/weekly/Predict.txt'
COMMENT_CHARS = '#:'

drawing = Drawing(400, 200)
data = []
for line in urlopen(URL).readlines():
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])
        
"""
drawing = Drawing(400, 200)
data = [
    (2007, 8, 113.2, 114.2, 112.2),
    (2007, 9, 112.8, 115.8, 109.8),
    (2007, 10, 111.0, 116.0, 106.0),
    (2007, 11, 109.8, 116.8, 102.8),
    (2007, 12, 107.3, 115.3, 99.3),
    (2008, 1, 105.2, 114.2, 96.2),
    (2008, 2, 104.1, 114.1, 94.1),
    (2008, 3, 99.9, 110.9, 88.9),
    (2008, 4, 94.8, 106.8, 82.8),
    (2008, 5, 91.2, 104.2, 78.2)
]

pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
times = [row[0] + row[1]/12.0 for row in data]

print pred
print high
print low
print times

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [zip(times, pred), zip(times, high), zip(times, low)]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)
drawing.add(String(250, 150, 'Sunspots',
                   fontSize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'reportlab.pdf', 'Sunspots')
print "Finished...."
