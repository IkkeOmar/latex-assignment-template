PDF := main.pdf

all: $(PDF)

$(PDF): main.tex preamble.tex $(wildcard q*.tex) $(wildcard fig/*.pdf)
	tectonic --keep-intermediates --outdir . main.tex

clean:
	rm -f main.pdf main.aux main.out main.toc

watch:
	ls q*.tex preamble.tex | xargs -n1 echo

.PHONY: all clean watch
