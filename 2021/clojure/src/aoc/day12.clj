(ns aoc.day12
  (:require [aoc.lib :as lib]))

(defn conta [coll, c] (some #(= c %) coll))

(defn h1 [cur p]
 (if (not= (first p) (last cur))
   []
   (if (or (= "end" (first cur) (= "end" (last cur))))
     []
     (if (= "end" (second p))
      [[] (conj cur (second p))]
      (let [p1 (second p)]
        (if (and (> (int (first p1)) 96) (< (int (first p1)) 123))
          (let [cc (conta cur, p1)]
            (if cc
              []
              [(conj cur p1) []]))
          [(conj cur p1) []]))))))

(defn help1 [paths ways done]
  (if (empty? ways)
    (count done)
    (let [cur (first ways)
          res-wd (for [p paths] (h1 cur p))
          w2 (map first (filter #(not (empty? (first %))) res-wd))
          d2 (map second (filter #(not (empty? (second %))) res-wd))
          w3 (concat w2 (rest ways))
          d3 (concat done d2)]
      ;(println "  cur " cur "  ::::" res-wd)
      ;(println "  :w::" ways w2)
      ;(println "  :d::" done d2)
      (println ":w3:" w3)
      (println ":d3:" d3)
      (help1 paths w3 d3))))

(defn part1 [lines]
  (let [path1 (map #(clojure.string/split % #"-") lines)
        path2 (map (fn [x] [(second x) (first x)]) path1)
        path3 (into path1 path2)
        ways (filter #(= "start" (first %)) path3)
        ;path4 (filter #(and (not= "start" (first %)) (not= "start" (second %) (not= "end" (first %)))) path3)]
        path4 (filter #(not= "start" (first %)) path3)
        path5 (filter #(not= "start" (second %)) path4)
        path6 (filter #(not= "end" (first %)) path5)]
        ;(println "path3" path3 (count path3))
        (println "ways " ways (count ways))
        ;(println "paths" path4 (count path4))
        ;(println "paths" path5 (count path5))
        (println "paths" path6 (count path6))
  (help1 path6 ways [])))

(defn help2 [lines idx]
  ;(println idx "|" lines)
  0)

(defn part2 [lines]
  (help2 lines 0))

(defn run [filename]
  (let [lines (lib/lines-str filename)]
    (time (println "Part 1: " (part1 lines)))
    (time (println "Part 2: " (part2 lines)))))
