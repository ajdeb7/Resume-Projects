import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * AUTHOR: Andrew deBerardinis
 * FILE: PA11Main.java
 * Project: Traveling Salesperson
 * PURPOSE: This program uses multiple different approaches to solve the
 * Traveling Salesperson Problem. This program utilizes the Heuristic and
 * Recursive Backtracking approach to find the cost and visit order of
 * each city in the Trip.
 * 
 * Usage Commands:
 * Input: HEURISTIC,BACKTRACK,MINE,TIME
 * Outputs: Lowest cost using the three approaches and how long each approach
 * took to find the lowest cost.
 *
 * --------EXAMPLE INPUT--------
 * Input File:
 * %%MatrixMarket matrix coordinate real general
 * %-------------------------------------------------------------------------------
 * % Driving distances between some cities in AZ.
 * % 1: Tucson
 * % 2: Phoenix
 * % 3: Prescott
 * % 4: Show Low
 * % 5: Flagstaff
 * %
 * % author: Michelle Strout
 * % kind: directed weighted graph
 * %-------------------------------------------------------------------------------
 * 5 5 20
 * 1 2 113.0
 * 2 1 113.0
 * 1 5 209.48
 * 5 1 209.48
 * 2 5 144.38
 */

public class PA11Main {
    public static void main(String[] args) {
        Scanner in = null;
        String line = "";
        List<String> file = new ArrayList<String>();
        Trip myTrip = null;
        Trip minTrip = new Trip(0);
        try {
            in = new Scanner(new File(args[0]));
            line = in.nextLine();
        } catch (FileNotFoundException ex) {
            ex.printStackTrace();
        }
        DGraph graph = createGraph(in, line, file);
        myTrip = new Trip(graph.getNumNodes());
        if (args[1].equals("BACKTRACK")) {
            minTrip = recursiveBack(graph, myTrip, minTrip);
            System.out.println(minTrip.toString(graph));
        } else if (args[1].equals("HEURISTIC")) {
            myTrip.chooseNextCity(1);
            minTrip = heuristic(graph, myTrip, minTrip);
            System.out.println(minTrip.toString(graph));
        } else if (args[1].equals("TIME")) {
            time(graph, myTrip, minTrip);
        } else if (args[1].equals("MINE")) {
            myTrip.chooseNextCity(1);
            minTrip = mine(graph, myTrip, minTrip);
            System.out.println(minTrip.toString(graph));
        }
    }

    /**
     * Purpose: This method creates a graph out of nodes using each line of
     * the input file(my created list).
     * 
     * @param in,
     *            input file
     * @param line,
     *            a single line in the file
     * @param file,
     *            empty list to add each line of the file to
     *            @return, graph with correct nodes, edges, and weights
     */
    public static DGraph createGraph(Scanner in, String line,
            List<String> file) {
        DGraph graph = null;
        // TODO: Skip over comment lines that can be at the beginning of mtx
        while (in.hasNextLine()) {
            line = in.nextLine();
            if (line.charAt(0) == '%') {
            } else {
                file.add(line);
            }
        }
        // TODO: Read the number of rows, columns and non-zeros
        String[] rowcolList = file.get(0).split("\\s+");
        int rows = Integer.parseInt(rowcolList[0]);
        int columns = Integer.parseInt(rowcolList[1]);

        // TODO: Initialize the graph using the number of nodes
        if (rows >= columns) {
            graph = new DGraph(rows);
        }
        if (columns >= rows) {
            graph = new DGraph(columns);
        }

        // TODO: Assuming the number of non-zeros reported is correct,
        // loop over the entry lines and add the directed edge,
        // do not include self edges.
        String[] lis = null;
        for (int i = 1; i < file.size(); i++) {
            lis = file.get(i).split("\\s+");
            graph.addEdge(Integer.parseInt(lis[0]), Integer.parseInt(lis[1]),
                    Double.parseDouble(lis[2]));
        }
        return graph;
    }

    /**
     * Purpose: Recursively backtracks to go through all possibilities to find
     * the best possible result(lowest cost).
     * 
     * @param graph,
     *            graph created and returned in createGraph
     * @param myTrip,
     *            created trip with correct number of cities from main
     * @param minTrip,
     *            created trip with no cities from main
     *            @return, trip with lowest cost
     */
    public static Trip recursiveBack(DGraph graph, Trip myTrip, Trip minTrip) {
        myTrip.chooseNextCity(1);
        minTrip = enumerate(graph, myTrip, minTrip);
        return minTrip;
    }

    /**
     * Purpose: Helper method for recursiveBack method to enable the
     * complete recursive backtracking to find best possible result.
     * 
     * @param graph,
     *            graph created and returned in createGraph
     * @param myTrip,
     *            created trip with correct number of cities from main
     * @param minTrip,
     *            created trip with no cities from main
     *            @return, trip with lowest cost
     */
    public static Trip enumerate(DGraph graph, Trip myTrip, Trip minTrip) {
        if (myTrip.citiesLeft().isEmpty()) {
            if (myTrip.tripCost(graph) < minTrip.tripCost(graph)) {
                minTrip.copyOtherIntoSelf(myTrip);
            }
            return minTrip;
        }

        if (myTrip.tripCost(graph) < minTrip.tripCost(graph)) {
            for (int i = 0; i < myTrip.citiesLeft().size(); i++) {
                myTrip.chooseNextCity(myTrip.citiesLeft().get(i));
                enumerate(graph, myTrip, minTrip);
                myTrip.unchooseLastCity();
            }
        }
        return minTrip;
    }

    /**
     * Purpose: Method using heuristic approach. Finds first available option.
     * 
     * @param graph,
     *            graph created and returned in createGraph
     * @param myTrip,
     *            created trip with correct number of cities from main
     * @param minTrip,
     *            created trip with no cities from main
     *            @return, trip with lowest cost
     */
    public static Trip heuristic(DGraph graph, Trip myTrip, Trip minTrip) {
        int currCity = 1;
        int bestN = 0;
        for (int k = 2; k <= graph.getNumNodes(); k++) {
            minTrip = new Trip(0);
            for (int neighbor : graph.getNeighbors(currCity)) {
                if (myTrip.isCityAvailable(neighbor)) {
                    myTrip.chooseNextCity(neighbor);
                    if (myTrip.tripCost(graph) < minTrip.tripCost(graph)) {
                        bestN = neighbor;
                        minTrip.copyOtherIntoSelf(myTrip);
                    }
                    myTrip.unchooseLastCity();
                }
            }
            myTrip.chooseNextCity(bestN);
            currCity = bestN;
        }
        return minTrip;
    }

    /**
     * Purpose: Recursively backtracks to go through all possibilities to find
     * the best possible result(lowest cost).
     * 
     * @param graph,
     *            graph created and returned in createGraph
     * @param myTrip,
     *            created trip with correct number of cities from main
     * @param minTrip,
     *            created trip with no cities from main
     *            @return, trip with lowest cost
     */
    public static Trip mine(DGraph graph, Trip myTrip, Trip minTrip) {
        if (myTrip.citiesLeft().size() == 0) {
            if (myTrip.tripCost(graph) < minTrip.tripCost(graph)) {
                minTrip.copyOtherIntoSelf(myTrip);
            }
            return minTrip;
        }

        if (myTrip.tripCost(graph) < minTrip.tripCost(graph)) {
            for (int i = 0; i < myTrip.citiesLeft().size(); i++) {
                myTrip.chooseNextCity(myTrip.citiesLeft().get(i));
                mine(graph, myTrip, minTrip);
                myTrip.unchooseLastCity();
            }
        }
        return minTrip;
    }

    /**
     * Purpose: Times heuristic, mine, and recursive backtracking approaches
     * and prints those times along with the lowest cost each approach found.
     * 
     * @param graph,
     *            graph created and returned in createGraph
     * @param myTrip,
     *            created trip with correct number of cities from main
     * @param minTrip,
     *            created trip with no cities from main
     */
    public static void time(DGraph graph, Trip myTrip, Trip minTrip) {
        long startTime = System.nanoTime();
        myTrip.chooseNextCity(1);
        Trip bestTrip = heuristic(graph, myTrip, minTrip);
        long endTime = System.nanoTime();
        long duration = (endTime - startTime) / 1000000;
        System.out.println("heuristic: cost = " + bestTrip.tripCost(graph)
                + ", " + duration + " milliseconds");
        long startTime2 = System.nanoTime();
        myTrip = new Trip(graph.getNumNodes());
        minTrip = new Trip(0);
        myTrip.chooseNextCity(1);
        Trip bestTrip2 = mine(graph, myTrip, minTrip);
        long endTime2 = System.nanoTime();
        long duration2 = (endTime2 - startTime2) / 1000000;
        System.out.println("mine: cost = " + bestTrip2.tripCost(graph) + ", "
                + duration2 + " milliseconds");
        long startTime1 = System.nanoTime();
        myTrip = new Trip(graph.getNumNodes());
        minTrip = new Trip(0);
        Trip bestTrip1 = recursiveBack(graph, myTrip, minTrip);
        long endTime1 = System.nanoTime();
        long duration1 = (endTime1 - startTime1) / 1000000;
        System.out.println("backtrack: cost = " + bestTrip1.tripCost(graph)
                + ", " + duration1 + " milliseconds");

    }
}