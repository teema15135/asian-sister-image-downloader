from threading import Thread
import requests
import os
import shutil

subDirectory = input("Enter sub-directory: ")

while True:
    code = input("Enter a code: ")
    try:
        int(code)
    except:
        print("Please provide a valid code...")
        print()
        continue

    r = requests.get(f'https://www.asiansister.com/tool/getImageDownload.php?code={code}')

    urls = r.text.split(',')

    if len(urls) == 1:
        print(f'No collection have {code} code...')
        print()
        continue

    count = 0
    completeCount = 0
    folderName = f'ASIAN SISTER - {code} - Download'
    if subDirectory != '':
        folderName = f'{subDirectory}/{folderName}'
    fileNamePrefix = 'image_'
    fileCount = len(urls) - 1

    indicator = ['-' for i in range(fileCount)]

    outputDirectory = folderName + '/'

    

    if not os.path.exists(os.path.dirname(outputDirectory)):
                try:
                    os.makedirs(os.path.dirname(outputDirectory))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
    else:
        print(f"You already have {outputDirectory} directory...")
        print()
        continue

    urls = urls[1:len(urls)]

    def req_get(url, localCount):
        global completeCount
        c = localCount
        img = requests.get(url, stream=True)
        outputPath = f'{outputDirectory}{fileNamePrefix}{c}.jpg'
        localFile = open(outputPath, 'wb')
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, localFile)
        indicator[c] = '*'
        completeCount += 1

    for url in urls:
        Thread(target=req_get, args=(url, count)).start()
        count += 1


    while completeCount < fileCount:
        print('\r' + (''.join(indicator)), end='')
    print('\r' + (''.join(indicator)))
    print("Download Complete!!!!")
    print()