import helper
import authorization
import alexa_device
import snowboy.snowboydecoder as snowboydecoder

__author__ = "NJC"
__license__ = "MIT"
__version__ = "0.2"


def user_input_loop(alexa_device):
    """ This thread initializes a voice recognition event based on user input. This function uses command line
        input for interacting with the user. The user can start a recording, or quit if desired.

        This is currently the "main" thread for the device.
    """
    # While the stop event is not set
    while True:
        model = 'files/alexa.umdl'
        detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
        print('Listening... Press Ctrl+C to exit')
        
        # main loop
        detector.start(detected_callback=alexa_device.user_initiate_audio,
                       sleep_time=0.03)
        
    detector.terminate()


if __name__ == "__main__":
    # Load configuration file (contains the authorization for the user and device information)
    config = helper.read_dict('config.dict')
    # Check for authorization, if none, initialize and ask user to go to a website for authorization.
    if 'refresh_token' not in config:
        print("Please go to http://localhost:5000")
        authorization.get_authorization()
        config = helper.read_dict('config.dict')

    # Create alexa device
    alexa_device = alexa_device.AlexaDevice(config)

    user_input_loop(alexa_device)

    print("Done")