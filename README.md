# termanim

My experiments with animation in the terminal, using ANSI escape sequences.

This project is meant to be a more structured approach to [anim.py](https://gist.github.com/sahasatvik/624a92563cbaf567c510c80b31326d56),
which implements effects such as transparency, colour gradients, fade-in, and movement.

## modules
- `termanim.ansi`: The _ANSICodes_ class lists useful ANSI codes for operating on the terminal screen.
- `termanim.term`: The _TermScreen_ class gives an interface for drawing to the terminal screen, with coloured text.
The _TermScreenRGB_ class allows the use of 24 bit RGB colour, with transparency effects.
The _TermThings_ class conveniently creates and modifies drawable text and box objects.
- `termanim.anim`: The _Effects_ class creates animation effects, which act on drawable objects and generate animation frames.

- `termanim.shm` : A demo animation of a block performing simple harmonic motion on the screen. Run `python3 -m termanim.shm`.

![SHM](https://user-images.githubusercontent.com/16478483/117474574-ad198800-af78-11eb-8c20-667f42fac931.gif)

- `termanim.shmRGB` : A demo animation of simple harmonic motion, this time with RGB colours. Run `python3 -m termanim.shmRGB`.

![SHMRGB](https://user-images.githubusercontent.com/16478483/117535208-52cd0580-b012-11eb-8917-fa655f1be1a3.gif)
