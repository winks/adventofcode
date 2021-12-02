(ns aoc.day01
  (:require [aoc.lib :as lib]))

(defn help1 [lines cur rv]
  ;(println i "|" cur "|" lines)
  (if (empty? lines)
    rv
    (if (> (first lines) cur)
      (help1 (rest lines) (first lines) (inc rv))
      (help1 (rest lines) (first lines) rv))))

(defn help2 [lines cur idx rv]
  ;(println rv " |idx: " idx " |sum: " cur " | " lines)
  (if (> idx (- (count lines) 3))
    rv
    (let [hd1 (nth lines idx)
          hd3 (nth lines (+ 2 idx))]
      (if (> hd3 cur)
        (help2 lines hd1 (inc idx) (inc rv))
        (help2 lines hd1 (inc idx) rv)))))

(defn part1 [lines]
  (help1 (rest lines) (first lines) 0))

(defn part2 [lines]
  (help2 lines 0 0 -1))

(defn run [filename]
  (let [lines (lib/lines-int filename)]
    (time (println "Part 1: " (part1 lines)))
    (time (println "Part 2: " (part2 lines)))))
