(ns aoc.day07
  (:require [aoc.lib :as lib]))

(defn tri [n]
  (/ (+ n (* n n)) 2))

(defn calc [nums fun]
  (let [r (range (apply min nums) (inc (apply max nums)))
        v (for [ar r] (for [n nums] (let [x (- ar n)] (fun (if (< 0 x) x (* -1 x))))))
        t (map #(reduce + %) v)]
  (apply min t)))

(defn run [filename]
  (let [lines (lib/lines-str filename)
        nums (lib/csv (first lines))]
    (time (println "Part 1: " (calc nums identity)))
    (time (println "Part 2: " (calc nums tri)))))
