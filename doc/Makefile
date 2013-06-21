VERSION := $(shell cat ../VERSION)
TARGET := ask-manual-$(VERSION).pdf

all: $(TARGET)

$(TARGET): ask-manual.tex
	pdflatex -shell-escape ask-manual.tex 
	mv ask-manual.pdf $(TARGET)

clean:
	rm -rf $(TARGET) *.log *.out *.toc *.aux

