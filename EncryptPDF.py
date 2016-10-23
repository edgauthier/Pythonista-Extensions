#! python2
# coding: utf-8

import appex
import console
import os
import keychain
import sys

from PyPDF2 import PdfFileReader,PdfFileWriter

def main():
  if not appex.is_running_extension():
    print('This script is intended to be run from the sharing extension.')
    return
  file_path = appex.get_file_path()
  if not file_path:
    print('No file found.')
    return
    
  console.hud_alert('Encrypting PDF...', duration=1)

  file_name = os.path.basename(file_path)

  with open(file_path, 'rb') as source_file:
    source_pdf = PdfFileReader(source_file)
    dest_pdf = get_pdf_file_writer(source_pdf)

    dest_pdf.encrypt(get_encryption_password())

    with open(file_name,'wb') as dest_file:
      dest_pdf.write(dest_file)

    console.open_in(dest_file.name)
    os.unlink(dest_file.name)
    appex.finish()

def get_pdf_file_writer(reader):
  # Get page count from writer and reader
  writer = PdfFileWriter()
  reader_num_pages = reader.getNumPages()
  writer_num_pages = writer.getNumPages()

  # Copy pages from reader to writer
  for rpagenum in range(0, reader_num_pages):
      reader_page = reader.getPage(rpagenum)
      writer.addPage(reader_page)
      writer_page = writer.getPage(writer_num_pages+rpagenum)
      
  return writer
  
def get_encryption_password():
  password = keychain.get_password('EncryptedPDFs', 'password')
  if password:
    return password.encode('ascii')
  password = console.secure_input('Enter password to encrypt PDFs: ').rstrip()
  keychain.set_password('EncryptedPDFs','password',password)
  return password

if __name__ == '__main__':
  main()
