import { Message } from './message_model'

export const dummy_messages: Message[] = [
    new Message("core", "DEBUG", "09:51:10", "this is s a test message 0"),
    new Message("core", "DEBUG", "09:51:11", "this is s a test message 1"),
    new Message("core", "INFO",  "09:51:12", "INFO test message"),
    new Message("core", "WARNING",  "09:51:13", "WARNING test message"),
    new Message("core", "ERROR",  "09:51:14", "ERROR test message"),
    new Message("account", "ERROR",  "09:51:14", "account ERROR test message"),
    new Message("account", "INFO",  "09:51:14", "account INFO test message"),
    new Message("celery", "DEBUG",  "09:51:14", "celery DEBUG test message"),
  ];

