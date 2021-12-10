(ns aoc.day10
  (:require [aoc.lib :as lib]))

(def ops  { \) \(  \] \[  \}   \{  \> \<    })
(def errs { \)  3  \] 57  \} 1197  \> 25137 })
(def p2pt { \(  1  \[ 2   \{    3  \< 4     })

(defn help1 [line stack]
  (if (= 0 (count line))
    [0 stack]
    (let [c (first line)]
      (if (get errs c)
        (if (= (last stack) (get ops c))
          (help1 (rest line) (pop stack))
          [(get errs c) []])
        (help1 (rest line) (conj stack c))))))

(defn help2 [line rv]
  (if (= 0 (count line))
    rv
    (let [c (last line)]
      (if (get p2pt c)
        (help2 (pop line) (+ (get p2pt c) (* 5 rv)))
        0))))

(defn part1 [lines]
  (reduce +
    (map first
      (for [line lines]
        (help1 line [])))))

(defn part2 [lines]
  (let [all (let [lines (for [line lines] (help1 line []))
                  noerr (filter #(= 0 (first %)) lines)]
              (for [line noerr]
                (help2 (second line) 0)))
        len (/ (count all) 2)]
    (nth (sort all) len)))

(defn run [filename]
  (let [lines (lib/lines-str filename)]
    (time (println "Part 1: " (part1 lines)))
    (time (println "Part 2: " (part2 lines)))))
