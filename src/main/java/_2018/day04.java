package _2018;

import static org.junit.Assert.assertEquals;
import java.util.*;
import java.util.Map.Entry;
import template.day;
import util.Global;
import util.Util;

public class day04 extends day {

  // <ID, <sleepMinute, Count>>
  Map<Integer, Map<Integer, Integer>> sleepCounts = new HashMap<>();

  // <ID, numTimesAsleep>
  Map<Integer, Integer> sleepAmount = new HashMap<>();

  public void presolve(List<String> input) {

    Collections.sort(input);
    sleepCounts = new HashMap<>();
    sleepAmount = new HashMap<>();

    int id = 0; // guard's id
    int pMinute = 0; // previous minute (for looping)
    for (String s : input) {
      String[] tokens = s.split("]");
      String[] datetimes = tokens[0].split(" ");
      // String[] dates = datetimes[0].split("-");
      // int year = Integer.parseInt(dates[0].substring(1, dates[0].length()));
      // int month = Integer.parseInt(dates[1]);
      // int day = Integer.parseInt(dates[2]);

      String[] times = datetimes[1].split(":");
      // int hour = Integer.parseInt(times[0]);
      int minute = Integer.parseInt(times[1]);

      String[] actions = tokens[1].split(" ");
      // System.out.println(year + " " + month + " " + day + " " + hour + " " + minute + " | " +
      // Arrays.asList(actions));

      // new guard
      if (actions.length == 5) {
        id = Integer.parseInt((actions[2].substring(1, actions[2].length())));
      } else { // sleep/wake

        switch (actions[1]) {
          case "falls":
            break;

          case "wakes":
            sleepAmount.merge(id, 1, Integer::sum); // sleepAmount[id]++;

            for (int i = pMinute; i < minute; i++) {
              // sleepCounts[id][p]++;
              // 3verbose5me
              sleepCounts.putIfAbsent(id, new HashMap<>());
              Map<Integer, Integer> temp = sleepCounts.get(id);
              temp.put(i, temp.getOrDefault(i, 0) + 1);
            }
            // System.out.println("Guard " + id + " slept for " + (minute - pMinute) + " minutes");
            break;

          default:
            break;
        }
      }
      pMinute = minute;
    }
  }

  @Override
  public String solve(List<String> input, boolean partTwo) {
    return "";
  }

  // find the guard with the most sleep minutes
  // find that guard's most likely minute of sleep
  // return guardID * minute of sleep
  @Override
  public String partOne(List<String> input) {

    // guard w/ most minutes of sleep
    int maxSleep = -1;
    int maxSleepGuardID = -1;
    for (Entry<Integer, Map<Integer, Integer>> sc : sleepCounts.entrySet()) {
      // System.out.println(sc);

      int tempID = sc.getKey();

      int sleepForGuard = 0;
      for (Entry<Integer, Integer> gsa : sc.getValue().entrySet()) {
        sleepForGuard += gsa.getValue();
      }
      // System.out.println("Sleep for guard " + tempID + " is " + sleepForGuard);
      if (sleepForGuard > maxSleep) {
        maxSleepGuardID = tempID;
        maxSleep = sleepForGuard;
      }
    }
    // System.out.println("Guard " + maxSleepGuardID + " sleeps " + maxSleep + " times");


    // for that guard, find the minute they are most likely to be asleep
    // i.e. sleepCounts<maxSleepGuardID> with maximum key
    int mostFreqSleepAmount = -1;
    int mostFreqSleepMinute = -1;
    for (Entry<Integer, Integer> gsa : sleepCounts.get(maxSleepGuardID).entrySet()) {

    }

    int mostSleepMinute = Collections
        .max(sleepCounts.get(maxSleepGuardID).entrySet(), (e1, e2) -> e1.getValue() - e2.getValue())
        .getKey();
    System.out.println("Guard " + maxSleepGuardID + " mostly asleep for minute " + mostSleepMinute);


    String out = String.valueOf(maxSleepGuardID * mostSleepMinute);

    return out;
  }

  // find the guard most frequently asleep on the same minute
  // find the guard's most
  @Override
  public String partTwo(List<String> input) {

    // go over all the minutes for a guard
    // see which minutes has highest count

    // guard w/ most minutes of sleep
    int mostFrequentMinute = -1;
    int mostFrequentMinuteCount = -1;
    int maxSleepGuardID = -1;
    // for each guard
    for (Entry<Integer, Map<Integer, Integer>> guard : sleepCounts.entrySet()) {

      int minute = -1;
      int minuteFreq = -1;
      for (Entry<Integer, Integer> gsa : guard.getValue().entrySet()) {
        if (gsa.getValue() > minuteFreq) {
          minute = gsa.getKey();
          minuteFreq = gsa.getValue();
        }
      }

      if (minuteFreq > mostFrequentMinuteCount) {
        mostFrequentMinute = minute;
        mostFrequentMinuteCount = minuteFreq;
        maxSleepGuardID = guard.getKey();
      }
    }

    return String.valueOf(maxSleepGuardID * mostFrequentMinute);
  }

  public static void main(String[] args) {
    day a = new day04();

    if (args.length > 0) {
      // perform tests
      String filename = Global.testPath + "_2018/day04_00" + Global.testExt;
      List<String> input = Util.readFileIntoListString(filename);

      a.presolve(input);

      // Part 1
      assertEquals("240", a.partOne(input));

      // Part 2
      assertEquals("4455", a.partTwo(input));

      System.out.println("Tests successful!");
      return;
    }

    // Take input, turn into usable form
    String filename = Global.testPath + "_2018/day04_01" + Global.testExt;
    List<String> input = Util.readFileIntoListString(filename);
    a.presolve(input);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));

  }
}
