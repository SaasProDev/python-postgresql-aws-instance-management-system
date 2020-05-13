export class Message {
   module_name: string;
    levelname: string;
    levelno: number;
    xtime: string;
    message: string;

    static levels = {
        "NOTSET": 0,
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    };
    constructor(module_name, levelname, xtime, message) {
      this.module_name = module_name;
      this.levelname = levelname;
      this.xtime = xtime;
      this.message = message;
      this.levelno = Message.levels[levelname]
    }
}

