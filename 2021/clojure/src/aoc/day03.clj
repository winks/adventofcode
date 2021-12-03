(ns aoc.day03
  (:require [aoc.lib :as lib]))

(defn hl2 [lines]
  (let [len (count (first lines))]
    (for [i (range len)]
      (for [line lines]
        (nth line i)))))

(defn part1 [lines]
  (let [cols (hl2 lines)
        red (map count (for [x cols] (filter #(= \1 %) x)))
        cut (/ (count lines) 2.0)
        rvg (for [r red] (if (> cut r) \0 \1))
        rve (for [r red] (if (< cut r) \0 \1))]
    (apply * (map #(Integer/parseInt (apply str %) 2) [rvg rve]))))

(defn filter-index [lines idx crit]
  (filter (fn [x] (= crit (nth x idx))) lines))

(defn help2 [lines idx red msb]
  (if (= 1 (count lines))
    lines
    (let [cols (hl2 lines)
          red (map count (for [x cols] (filter #(= \1 %) x)))
          cut (/ (count lines) 2.0)
          pos (float (nth red idx))
          crit1 (if (or (< cut pos) (= cut pos)) \1 \0)
          crit (if msb crit1 (if (= \1 crit1) \0 \1))]
      (help2 (filter-index lines idx crit) (inc idx) red msb))))

(defn part2 [lines]
  (let [cols (hl2 lines)
        red (map count (for [x cols] (filter #(= \1 %) x)))
        ro (help2 lines 0 red true)
        rc (help2 lines 0 red false)]
    (apply * (map #(Integer/parseInt (apply str %) 2) [ro rc]))))

(defn run [filename]
  (let [lines (lib/lines-str filename)]
    (time (println "Part 1: " (part1 lines)))
    (time (println "Part 2: " (part2 lines)))))
