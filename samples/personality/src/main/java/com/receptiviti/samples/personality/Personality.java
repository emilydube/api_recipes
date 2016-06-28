package com.receptiviti.samples.personality;


import com.mashape.unirest.http.exceptions.UnirestException;
import org.kohsuke.args4j.Argument;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

import java.util.ArrayList;
import java.util.List;

public class Personality {

    @Option(name="-server", usage="name of server to use")
    private String server = "https://app.receptiviti.com";

    @Argument
    private List<String> arguments = new ArrayList<String>();

    public static void main(String[] args) {
        new Personality().doMain(args);
    }

    public void doMain(String[] args){
        Content content;
        Receptiviti receptiviti;
        Person person;
        List<String> Snapshot;

        CmdLineParser parser = new CmdLineParser(this);


        try {
            // parse the arguments.
            parser.parseArgument(args);

            if( arguments.size() != 3 )
                throw new CmdLineException(parser, "Error: 3 arguments expected\n");

        } catch( CmdLineException e ) {
            System.err.println(e.getMessage());
            System.err.println("java -jar personality.jar [options...] key secret file");
            parser.printUsage(System.err);
            System.err.println();
            System.err.println("  Example: java Personality <your api key> <your api secret key> <file to process>");

            return;
        }

        content = new Content(arguments.get(2));

        if (content.content != null) {
            try {
                receptiviti = new Receptiviti(server, arguments.get(0), arguments.get(1));
                person = new Person(content.name, content.name, 0);
                person = receptiviti.GetPersonID(person);
                if (person.id == null) {
                    person = receptiviti.SavePerson(person);
                }
                content = receptiviti.AnalyseContent(person, content);

                System.out.println("person id: " + person.id);
                System.out.println("content id: " + content.id);
                System.out.println("personality profile:-");
                for (String s: content.snapshot) {
                    System.out.println(s);
                }
            } catch (UnirestException e) {
                System.err.println("Error communication with Receptiviti: " + e.getMessage());
            } catch (ReceptivitiExpection e) {
                System.err.println("Receptiviti error: " + e.getMessage());
            }
        }
    }
}
