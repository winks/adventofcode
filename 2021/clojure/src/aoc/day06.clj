(ns aoc.day06
  (:require [clojure.string :as str])
  (:require [aoc.lib :as lib]))

(defn prep [tank fish]
  (if (= 0 (count fish))
    tank
    (let [f (first fish)
          h (take f tank)
          t (take-last (- 8 f) tank)
          x (conj t (inc (nth tank f)) h)
          tank2 (flatten x)]
    (prep tank2 (rest fish)))))

(defn tick1 [tank]
  (let [t (rest tank)]
    (if (> (first tank) 0)
      (flatten [(take 6 t) (+ (first tank) (nth t 6)) (nth t 7) (first tank)])
      (flatten [t 0]))))

(defn help1 [tank runs]
  (if (= 0 runs)
    (reduce + tank)
    (let [tank2 (tick1 tank)]
      (help1 tank2 (dec runs)))))

(defn part1 [lines runs]
  (let [fish (map #(Integer/parseInt %) (str/split (first lines) #","))
        tank (vec (repeat 8 0))
        tank2 (prep tank fish)]
    (help1 tank2 runs)))

(defn run [filename]
  (let [lines (lib/lines-str filename)]
    (time (println "Part 1: " (part1 lines 80)))
    (time (println "Part 2: " (part1 lines 256)))))
