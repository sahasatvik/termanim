# termanim

My experiments with animation in the terminal, using ANSI escape sequences.
Although [anim.py](https://gist.github.com/sahasatvik/624a92563cbaf567c510c80b31326d56) is currently much more advanced, implementing
transparency, colour gradients, and fade-in effects, this project offers a more structured approach.

## modules
- `termanim.ansi`: The _ANSICodes_ class lists useful ANSI codes for operating on the terminal screen.
- `termanim.term`: The _TermScreen_ class gives an interface for drawing to the terminal screen, with coloured text.
The _TermScreenRGB_ class allows the use of 24 bit RGB colour, with transparency effects.
The _TermThings_ class conveniently creates and modifies drawable text and box objects.
- `termanim.shm` : A demo animation of a block performing simple harmonic motion on the screen. Run `python3 -m termanim.shm`.

![SHM](https://user-images.githubusercontent.com/16478483/117474574-ad198800-af78-11eb-8c20-667f42fac931.gif)
