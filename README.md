# Micro MVC Framework

## Overview

Tentatively calling this project "Cutesy MVC." I'll probably call the command-line utility component something masculine like "cutify." Taylor Otwell doesn't have anything on my ability to name things.

Literally developing this at least in the preliminary stages on repl.it on my phone. Just would like to practice python when I have the time, and also would be cool if the end product was something useful to me. 

Taking inspiration from two of my favorite projects: Laravel and React. Would also like to practice threading a bit, so my idea is to basically have a client-server model where the V of the MVC is on the main thread and the M and C of MVC are on a second thread. Rather than do a templating system for the UI system, I think I want to try to emulate basic features of React and create a component library agnostic UI component hierarchy system. These components on the main thread will generate request objects that are sent via queue to the server thread, which eventually sends back a response object via another queue.

Obviously being a solo project that draws inspiration from two major projects, I am not implementing all of the features of React and Laravel. For example, I am creating systems to migrate, query, and model data from SQLite, but I am not building support for any other database systems.

## Docs

Markdown formatted documentation files can be found in the docs folder.