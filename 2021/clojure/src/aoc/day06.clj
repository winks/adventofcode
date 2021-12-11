(ns aoc.day06
  (:require [clojure.string :as str])
  (:require [aoc.lib :as lib]))

(defn prep [tank fish]
  (if (= 0 (count fish))
    tank
    (let [f (first fish)
          h (take f tank)
          t (take-last (- 8 f) tank)]
    (prep (flatten [h (inc (nth tank f)) t]) (rest fish)))))

(defn tick [tank]
  (let [t (rest tank)]
    (if (> (first tank) 0)
      (flatten [(take 6 t) (+ (first tank) (nth t 6)) (nth t 7) (first tank)])
      (flatten [t 0]))))

(defn help [tank runs]
  (if (= 0 runs)
    (reduce + tank)
    (help (tick tank) (dec runs))))

(defn part1 [lines runs]
  (let [fish (map #(Integer/parseInt %) (str/split (first lines) #","))
        tank (prep (vec (repeat 8 0)) fish)]
    (help tank runs)))

(defn run [filename]
  (let [lines (lib/lines-str filename)]
    (time (println "Part 1: " (part1 lines 80)))
    (time (println "Part 2: " (part1 lines 256)))
    (let [fish (map #(Integer/parseInt %) (str/split (first lines) #","))
          tank (prep (vec (repeat 8 0)) fish)]
      (time (println (help tank 80)))
      (time (println (help tank 256)))
    )))
