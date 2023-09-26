# Credit to jsheedy for this script. Original can be found at:
# https://gist.github.com/jsheedy/ed81cdf18190183b3b7d
# Useful for using copy_from in psycopg2 without actually writing to a file.

import io
import sys
from logger import getLogger


class IteratorFile(io.TextIOBase):
    """ given an iterator which yields strings,
    return a file like object for reading those strings """

    def __init__(self, it):
        self._it = it
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):

        logger = getLogger('iterator_file.read')
        try:
            while self._f.tell() < length:
                self._f.write(next(self._it) + "\n")

        except StopIteration as e:
            # soak up StopIteration. this block is not necessary because
            # of finally, but just to be explicit
            pass

        except Exception as e:
            logger.error(f"uncaught exception: {e}", exc_info=True)

        finally:
            self._f.seek(0)
            data = self._f.read(length)

            # save the remainder for next read
            remainder = self._f.read()
            self._f.seek(0)
            self._f.truncate(0)
            self._f.write(remainder)
            return data

    def readline(self):
        return next(self._it)
