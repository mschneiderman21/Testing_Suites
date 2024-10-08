import AI_SENSOR_ttsAPI

def main():
    print("This is to retrive the image from the tts server")

    uplinks = AI_SENSOR_ttsAPI.get_uplinks(1)

    print(uplinks)


if __name__ == "__main__":
    main()