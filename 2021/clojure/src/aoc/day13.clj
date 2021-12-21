(ns aoc.day13
  (:require [aoc.lib :as lib]))

(defn pp [paper]
  (doall (for [line paper] (println (clojure.string/replace (apply str line) #"\.+$" "")))))

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
          mid (str (subs (nth paper yy2) 0 xx2) "#" (subs (nth paper yy2) (inc xx2)))
          tlx (take-last (dec (- py yy2)) (take py paper))
          paper2 (into (into (vec (take yy2 paper)) [mid]) tlx)]
      (cc (rest points) paper2 px py))))

(defn calc [lines p1]
  (let [all-folds (filter #(= \f (first %)) lines)
        folds (if p1 [(first all-folds)] all-folds)
        folds-x (count (filter #(= \x (nth % 11)) folds))
        folds-y (- (count folds) folds-x)
        points (map lib/csv (filter #(not (= \f (first %))) lines))
        max-x (inc (apply max (map first points)))
        max-y (inc (apply max (map second points)))
        ffx (reduce * (repeat folds-x 2))
        ffy (reduce * (repeat folds-y 2))
        part-x (dec (/ (inc max-x) ffx))
        part-y (dec (/ (inc max-y) ffy))
        paper2 (repeat max-y (apply str(repeat max-x ".")))
        paper3 (cc points paper2 part-x part-y)]
  (if p1
    (count (filter #(= \# %) (apply str (flatten paper3))))
    (do (pp paper3) ""))))

(defn run [filename]
  (let [lines (filter #(> (count %) 0) (lib/lines-str filename))]
    (time (println "Part 1: " (calc lines true)))
    (time (println "Part 2: " (calc lines false)))))
