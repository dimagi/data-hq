"""
Tests for the multiple file upload widget and field.

Created by Edward Dale (www.scompt.com)
Released into the Public Domain
"""

from django.utils.datastructures import MultiValueDict
from django import newforms as forms
import unittest
from django.test.client import Client
from django.test import TestCase
from multifile import *

class MultiFileInputTest(unittest.TestCase):
    """
    Tests for the widget itself.
    """
    
    def testBasics(self):
        """
        Make sure the basics are correct (needs_multipart_form & is_hidden).
        """
        m=MultiFileInput()
        
        self.assertTrue(m.needs_multipart_form)
        self.assertFalse(m.is_hidden)
    
    def testNoRender(self):
        """
        Makes sure we show a minimum of 1 input box.
        """
        m=MultiFileInput({'count':0})
        r=m.render(name='blah', value='bla', attrs={'id':'test'})
        
        self.assert_('<input type="file" name="blah[]" id="test0" />' in r)
        
    def testSingleRender(self):
        """
        Test the output of a single field being rendered.
        """
        m=MultiFileInput()
        r=m.render(name='blah', value='bla', attrs={'id':'test'})
        
        self.assert_('<input type="file" name="blah[]" id="test0" />' in r)
    
    def testMultiRender(self):
        """
        Tests that two input boxes are rendered when given a count of 2.
        """
        m=MultiFileInput({'count':2})
        r=m.render(name='blah', value='bla', attrs={'id':'test'})
        
        self.assert_('<input type="file" name="blah[]" id="test0" />' in r)
        self.assert_('<input type="file" name="blah[]" id="test1" />' in r)

class MultiFileFieldTest(unittest.TestCase):
    """
    Tests that MultiFileField field.
    """
    
    class OptionalForm(forms.Form):
        """
        A simple Form that has an optional MultiFileField.
        """
        files = MultiFileField(required=False)
    
    class RequiredForm(forms.Form):
        """
        A simple Form that has an required MultiFileField.
        """
        files = MultiFileField(required=True)
    
    class MultiForm(forms.Form):
        """
        A simple Form with a MultiFileField with 2 input boxes.
        """
        files = MultiFileField(count=2)
    
    class StrictForm(forms.Form):
        files = MultiFileField(count=2, strict=True)
    
    def testOneRender(self):
        """
        Test the rendering of a MultiFileField with 1 input box.
        """
        f = self.RequiredForm()
        p=f.as_p()
        
        self.assert_('<input type="file" name="files[]" id="id_files0" />' in p)
    
    def testTwoRender(self):
        """
        Test the rendering of a MultiFileField with 2 input boxes.
        """
        f = self.MultiForm()
        p=f.as_p()

        self.assert_('<input type="file" name="files[]" id="id_files0" />' in p)
        self.assert_('<input type="file" name="files[]" id="id_files1" />' in p)
        
    def testNoFiles(self):
        """
        Tests binding a Form with required and optional MultiFileFields.
        """
        f = self.RequiredForm({}, {})
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())
        
        f = self.OptionalForm({}, {})
        self.assertTrue(f.is_bound)
        self.assertTrue(f.is_valid())
    
    def testOneFile(self):
        """
        Tests the binding of a Form with a single file attached.
        """
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': 'www'}]})
        f = self.RequiredForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertTrue(f.is_valid())
        
        self.assertEquals(len(f.cleaned_data['files']), 1)
        self.assertEquals(f.cleaned_data['files'][0].filename, file_data['files[]']['filename'])
        self.assertEquals(f.cleaned_data['files'][0].content, file_data['files[]']['content'])
        
        f = self.OptionalForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertTrue(f.is_valid())
    
    def testTwoFile(self):
        """
        Tests the binding of a Form with two files attached.
        """
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': 'www'},{'filename':'lah.jpg', 'content': 'woop'}]})
        f = self.RequiredForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertTrue(f.is_valid())
        
        self.assertEquals(len(f.cleaned_data['files']), 2)
        for input_file in file_data.getlist('files[]'):
            found = False
            for output_file in f.cleaned_data['files']:
                found = found or (output_file.filename == input_file['filename'] and output_file.content == input_file['content'])
            self.assertTrue(found)
    
    def testEmptyFile(self):
        """
        Tests the binding of a Form with 1 empty file.
        """
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': ''}]})
        f = self.RequiredForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())
        
        f = self.OptionalForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())
    
    def testOneEmptyFile(self):
        """
        If any file is empty, then the whole form is invalid.
        """
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': 'www'},{'filename':'lah.jpg', 'content': ''}]})
        f = self.RequiredForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())
        
        f = self.OptionalForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())
    
    def testStrict(self):
        """
        Tests whether the strict attribute works to force a user to upload n files.
        """
        
        # 1 file is no good, we want 2
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': 'www'}]})
        f = self.StrictForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())        

        # 2 files is great, we want 2
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': 'www'},{'filename':'lah.jpg', 'content': 'asdf'}]})
        f = self.StrictForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertTrue(f.is_valid())        

        # 3 files is no good, we want 2
        file_data = MultiValueDict({'files[]': [{'filename':'face.jpg', 'content': 'www'},{'filename':'lah.jpg', 'content': 'asdf'}, {'filename':'blah.jpg', 'content': 'asdf'}]})
        f = self.StrictForm({}, file_data)
        self.assertTrue(f.is_bound)
        self.assertFalse(f.is_valid())        
    
    def testBind(self):
        """
        Tests the binding of the form.  Probably not necessary.
        """
        file_data = {'files': {'filename':'face.jpg', 'content': ''}}
        f = self.RequiredForm()
        self.assertFalse(f.is_bound)
        
        f = self.RequiredForm({}, file_data)
        self.assertTrue(f.is_bound)

class FixedMultiFileTest(unittest.TestCase):
    def testSingleRender(self):
        """
        Test the output of a single field being rendered.
        """
        m=FixedMultiFileInput()
        r=m.render(name='blah', value='bla', attrs={'id':'test'})

        self.assertEquals('<input type="file" name="blah[]" id="test0" />\n', r)