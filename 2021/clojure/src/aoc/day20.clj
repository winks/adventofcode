(ns aoc.day20
  (:require [aoc.lib :as lib]))

(defn pp "pretty print" [im]
  (doall (for [row im] (println row)))
  (println "--"))

(defn pad "pad the image with a margin of <offset> dots all around" [im lrow trow offset]
  (let [mid (for [row im] (str lrow row lrow))]
  (concat (repeat offset trow) mid (repeat offset trow))))

(defn exp "exponent - x ^ n" [x n]
  (reduce * (repeat n x)))

(defn bin "convert string of '.#' to binary, .#.# = 0101 = 5" [s rv n]
  (if (empty? s)
    rv
    (let [pos (dec (count s))
          last (subs s pos)
          rest (subs s 0 pos)
          plus (if (= "#" last) (exp 2 n) 0)]
    (bin rest (+ rv plus) (inc n)))))

(defn new-tile "get algo pos of new tile at row y, column x" [image x y]
  (let [line-len (count (nth image y))
        firstx (if (<= x 1) 0 (dec x))
        lastx  (if (<= x (- line-len 3)) (+ 2 x) (- line-len 1))
        top (if (= 0 y) ""                   (subs (nth image (dec y)) firstx lastx))
        mid                                  (subs (nth image      y)  firstx lastx)
        bot (if (= (dec( count image)) y) "" (subs (nth image (inc y)) firstx lastx))]
  (bin (str top mid bot) 0 0)))

(defn step "proceed one step by going through the image by rows" [image algo]
  (let [line-len (count (first image))]
    (for [y (range (count image))]
      (loop [x 1 row2 ""]
        (if (> x (- line-len 3))
          (if (= \. (first row2)) (str \. row2 \. \.) (str \# row2 \# \#)) ; pretend the margin is infinity
          (recur (inc x) (str row2 (nth algo (new-tile image x y)))))))))

(defn counter "count the # in an image" [image]
  (let [s (for [row image] (count (clojure.string/replace row #"\." "")))]
    (reduce + s)))

(defn part1 "part1, actually also part2" [image algo runs]
  (let [offset (+ 5 runs)
        lrow (clojure.string/join (repeat offset \.))
        trow (str lrow (clojure.string/join (repeat (count (first image)) \.)) lrow)
        im2 (pad image lrow trow offset)
        im3 (loop [imx im2 r runs] (if (= 0 r) imx (recur (step imx algo) (dec r))))]
  (counter im3)))

(defn run [filename]
  (let [data (clojure.string/split (slurp filename) #"\n\n")
        algo (clojure.string/replace (first data) #"\n", "")
        lines (clojure.string/split-lines (second data))]
    (time (println "Part 1: " (part1 lines algo 2)))
    (time (println "Part 2: " (part1 lines algo 50)))))
