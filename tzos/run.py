# -*- coding: utf-8 -*-
"""
    tzos.run
    ~~~~~~~~~~~~~~

    Development server that runs TZOS

    :copyright: (c) 2011 Julen Ruiz Aizpuru.
    :license: BSD, see LICENSE for more details.
"""

from tzos import create_app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
