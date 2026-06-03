"""PodLens local web UI.

A self-service surface that runs entirely on your own machine: upload a
subtitle file, read the full interpretation (private layers included, because
it is local and only you see it), then confirm to publish the PUBLIC layers to
your site and push them live -- all without an agent in the loop.

It is a thin frontend over the same headless core the CLI uses
(`podlens.interpreter.interpret` + `podlens.publish`).
"""
