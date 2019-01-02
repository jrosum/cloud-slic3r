class SendToPrinter:

    def __init__(self, system, host, printer_name, api_key):
        self.printer_name = printer_name
        self.host = host
        self.api_key = api_key
        self.system = system

    def send_to_printer(self, folder_id, filename):
        path_to_file = "temp/{}/{}".format(folder_id, filename)
        curl_command = "curl -i -X POST -H \"Content-Type: multipart/form-data\" -H \"x-api-key: " + self.api_key + "\" -F \"a=upload\" -F \"filename=@[" + path_to_file + "]\" \"http://" + self.host + ":3344/printer/model/" + self.printer_name + "\""
        print(curl_command)
        return self.system(curl_command)