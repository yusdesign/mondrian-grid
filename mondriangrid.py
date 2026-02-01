#!/usr/bin/env python3
"""
MondrianGrid - Generated with INX Builder
"""

import inkex


class MondrianGrid(inkex.EffectExtension):
    """MondrianGrid extension"""
    
    def add_arguments(self, pars):
        pars.add_argument("--message", type=str, default="Hello World!", help="Test message")
    
    def effect(self):
        self.msg(f"{self.options.message} from {self.__class__.__name__}!")


if __name__ == '__main__':
    MondrianGrid().run()
