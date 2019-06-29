package _2018;

import java.util.*;
import java.util.Map.Entry;
import template.day;
import util.Global;
import util.Util;

// https://adventofcode.com/2018/day/4

// TODO : stream it up

public class day04 extends day {

  // <ID, <sleepMinute, Count>>
  Map<Integer, Map<Integer, Integer>> sleepCounts = new HashMap<>();

  public void presolve(List<String> input) {

    Collections.sort(input);
    sleepCounts = new HashMap<>();

    int id = 0; // guard's id
    int pMinute = 0; // previous minute (for looping)
    for (String s : input) {
      String[] tokens = s.split("]");
      String[] datetimes = tokens[0].split(" ");

      String[] times = datetimes[1].split(":");
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

    // Entry<Integer, Map<Integer, Integer>> a = Collections.max(
    // sleepCounts.entrySet().stream()
    // .mapToInt(es -> es.getValue().values().stream()
    // .mapToInt(i -> i).sum()).collect(Collectors.toList())
    // );

    // System.out.println("Guard: " + a.getKey() + ", sleep time: " + a.getValue());

    // guard w/ most minutes of sleep
    int maxSleep = -1;
    int maxSleepGuardID = -1;
    for (Entry<Integer, Map<Integer, Integer>> sc : sleepCounts.entrySet()) {
      // System.out.println(sc);

      int sleepForGuard = sc.getValue().values().stream().mapToInt(i -> i).sum();
      // System.out.println("Sleep for guard " + tempID + " is " + sleepForGuard);
      if (sleepForGuard > maxSleep) {
        maxSleepGuardID = sc.getKey();
        maxSleep = sleepForGuard;
      }
    }

    // for that guard, find the minute they are most likely to be asleep
    // i.e. sleepCounts<maxSleepGuardID> with maximum key
    int mostSleepMinute = Collections
        .max(sleepCounts.get(maxSleepGuardID).entrySet(), (e1, e2) -> e1.getValue() - e2.getValue())
        .getKey();
    System.out.println("Guard " + maxSleepGuardID + " mostly asleep for minute " + mostSleepMinute);

    return String.valueOf(maxSleepGuardID * mostSleepMinute);
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

      Entry<Integer, Integer> minuteStream =
          Collections.max(guard.getValue().entrySet(), (e1, e2) -> e1.getValue() - e2.getValue());

      int minute = minuteStream.getKey();
      int minuteFreq = minuteStream.getValue();

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

    // Take input, turn into usable form
    String filename = Global.testPath + "_2018/day04_01" + Global.testExt;
    List<String> input = Util.readFileIntoListString(filename);
    a.presolve(input);

    // Do something with the input and a
    System.out.println("Part 1: " + a.partOne(input));
    System.out.println("Part 2: " + a.partTwo(input));

  }
}
