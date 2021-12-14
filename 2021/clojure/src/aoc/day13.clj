(ns aoc.day13
  (:require [aoc.lib :as lib]))

(defn help1 [lines idx]
  ;(println idx "|" lines)
  0)



(defn pp [paper]
  (doall (for [line paper] (println (apply str line)))))

(defn cc [points paper px py]
  (if (empty? points)
    paper
    (let [point (first points)
          nx (int (/ (first point) (inc px)))
          ny (int (/ (second point) (inc py)))
          xx (- (first point) nx (* nx px))
          yy (- (second point) ny (* ny py))
          xx2 (if (= 1 (mod nx 2)) (- px xx 1) xx)
          yy2 (if (= 1 (mod ny 2)) (- py yy 1) yy)
          paper2 (for [fy (range 0 py)]
          (if (= yy2 fy)
          (concat (take xx2 (nth paper fy)) ["#"] (take-last (- px xx2 1) (nth paper fy)))
          (nth paper fy)))]

    (cc (rest points) paper2 px py))))

(defn calc [lines p1]
  (let [folds (filter #(= \f (first %)) lines)
        folds-x (count (filter #(= \x (nth % 11)) folds))
        folds-y (count (filter #(= \y (nth % 11)) folds))
        points (map lib/csv (filter #(not (= \f (first %))) lines))
        max-x (inc (apply max (map first points)))
        max-y (inc (apply max (map second points)))
        ffx (reduce * (repeat folds-x 2))
        ffy (reduce * (repeat folds-y 2))
        part-x (dec (/ (inc max-x) ffx))
        part-y (dec (/ (inc max-y) ffy))
        paper2 (take max-y (repeat (take max-x (repeat "."))))
        lll (println "LL" part-x part-y)
        paper3 (cc points paper2 part-x part-y)]
        (pp paper3)
  (count (filter #(= "#" %) (flatten paper3)))))
  ;(if (= [0 1] [fx fy]) (count (filter #(= "#" %) (flatten paper3))) (do (pp paper3) 0))))

(defn part1 [lines]
  (calc lines))

(defn run [filename]
  (let [lines (filter #(> (count %) 0) (lib/lines-str filename))]
    (time (println "Part 1: " (calc lines true)))
    (time (println "Part 2: " (calc lines false)))))
