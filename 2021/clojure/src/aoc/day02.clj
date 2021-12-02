(ns aoc.day02
  (:require [aoc.lib :as lib]))

(defn help1 [lines idx hp d]
  ;(println idx "|" hp "| " d)
  (if (> (inc idx) (count lines))
    (* hp d)
    (let [cur (nth lines idx)
          cmd (first cur)
          arg (Integer/parseInt (second cur))]
      (case cmd
        "forward" (help1 lines (inc idx) (+ hp arg) d)
        "up"      (help1 lines (inc idx) hp (- d arg))
        "down"    (help1 lines (inc idx) hp (+ d arg))))))

(defn help2 [lines idx hp d aim]
  ;(println idx "|" hp "| " d)
  (if (> (inc idx) (count lines))
    (* hp d)
    (let [cur (nth lines idx)
          cmd (first cur)
          arg (Integer/parseInt (second cur))]
    (case cmd
      "forward" (help2 lines (inc idx) (+ hp arg) (+ d (* aim arg)) aim)
      "up"      (help2 lines (inc idx) hp d (- aim arg))
      "down"    (help2 lines (inc idx) hp d (+ aim arg))))))

(defn help11 [lines hp d]
  ;(println idx "|" hp "| " d)
  (if (empty? lines)
    (* hp d)
    (let [cur (first lines)
          cmd (first cur)
          arg (Integer/parseInt (second cur))]
      (case cmd
        "forward" (help11 (rest lines) (+ hp arg) d)
        "up"      (help11 (rest lines) hp (- d arg))
        "down"    (help11 (rest lines) hp (+ d arg))))))

(defn help22 [lines hp d aim]
  ;(println idx "|" hp "| " d)
  (if (empty? lines)
    (* hp d)
    (let [cur (first lines)
          cmd (first cur)
          arg (Integer/parseInt (second cur))]
    (case cmd
      "forward" (help22 (rest lines) (+ hp arg) (+ d (* aim arg)) aim)
      "up"      (help22 (rest lines) hp d (- aim arg))
      "down"    (help22 (rest lines) hp d (+ aim arg))))))

(defn part1 [lines]
  (help1 lines 0 0 0))

(defn part2 [lines]
  (help2 lines 0 0 0 0))

(defn part11 [lines]
  (help11 lines 0 0))

(defn part22 [lines]
  (help22 lines 0 0 0))

(defn run [filename]
  (let [lines (map (fn [x] (clojure.string/split x #" ")) (lib/lines-str filename))]
    (time (println "Part 11: " (part11 lines)))
    (time (println "Part 22: " (part22 lines)))
    (time (println "Part 1: " (part1 lines)))
    (time (println "Part 2: " (part2 lines)))))
