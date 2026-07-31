#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `h8mail` package."""


import unittest
import tempfile
import os
import tarfile
import gzip
from h8mail.utils import run
from h8mail.utils import classes
from h8mail.utils import helpers
from h8mail.utils import localsearch
from h8mail.utils import localgzipsearch

def print_test_banner(testname):
    print("========================")
    print("========================")
    print("\tTESTING: "+testname)
    print("========================")
    print("========================")
    

class TestH8mail(unittest.TestCase):
    """Tests for `h8mail` package."""

    def setUp(self):
        """Generating local files with automatic cleanup (Python 3.10+)"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = self.temp_dir.name
        print(f"Created Temp Dir: {self.temp_path}")
        print(f"Registering dir + content for auto cleanup: {self.temp_path}")
        
        self.addCleanup(self.temp_dir.cleanup)


        # --- Dummy Data ---
        emails = """
        john.smith@gmail.com
        john.smith@gmail.com
        fijsdhkfnhqsdkf
        fdqfqsdff
        test@evilcorp.com
        notfound@email.com
        """

        creds = """
        john.smith@gmail.com:SecretPASS
        bloblfd
        fjsdkf,ds
        test@evilcorp.com:An0therSECRETpassw0rd
        ddqsdqs
        """


        self.filetargets = os.path.join(self.temp_path, "test-emails.txt")
        self.filetxt = os.path.join(self.temp_path, "test-creds.txt")
        self.filegz = os.path.join(self.temp_path, "test-creds.tar.gz")

        print("Test files generated in : " + self.temp_dir)

        with open(self.filetargets, "w", encoding="utf-8") as f:
            f.write(emails)

        with open(self.filetxt, "w", encoding="utf-8") as f:
            f.write(creds)

        with tarfile.open(self.filegz, "w:gz") as tar:
            tar.add(self.filetxt, arcname="test-creds.txt")

    def test_000_simple(self):
        """Simple test"""
        run.print_banner()
        print_test_banner("VANILLA")

        user_args = run.parse_args(["-t", "test@example.com"])
        run.h8mail(user_args)

    def test_002_local_files_txt_gz(self):
        """Local file search Test"""
        run.print_banner()
        print_test_banner("TXT LOCAL")
        user_args_lb = run.parse_args(["-t", self.filetargets, "-lb", self.filetxt, "-sk"])
        run.h8mail(user_args_lb)
        print_test_banner("TXT LOCAL-SINGLFILE")
        user_args_lb = run.parse_args(["-t", self.filetargets, "-lb", self.filetxt, "-sk", "-sf"])
        run.h8mail(user_args_lb)

        run.print_banner()
        print_test_banner("GZ LOCAL")
        user_args_gz = run.parse_args(["-t", self.filetargets, "-gz", self.filegz, "-sk"])
        run.h8mail(user_args_gz)
        print_test_banner("GZ LOCAL-SINGLEFILE")
        user_args_gz = run.parse_args(["-t", self.filetargets, "-gz", self.filegz, "-sk", "-sf"])
        run.h8mail(user_args_gz)

    def test_003_url(self):
        run.print_banner()
        print_test_banner("URL-RAW")
        user_args_lb = run.parse_args(["-u", "https://raw.githubusercontent.com/khast3x/h8mail/master/tests/test_email.txt"])
        run.h8mail(user_args_lb)
        run.print_banner()
        print_test_banner("URL-MESSY")
        user_args_lb = run.parse_args(["-u", "https://raw.githubusercontent.com/khast3x/h8mail/master/tests/test_email.txt"])
        run.h8mail(user_args_lb)
