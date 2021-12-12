(ns aoc.day11
  (:require [aoc.lib :as lib]))

(def nex [[-1 0] [-1 1] [0 1] [1 1] [1 0] [1 -1] [0 -1] [-1 -1]])
(def flashes (atom 0))

(defn help2 [lines idx]
  ;(println idx "|" lines)
  0)

(defn getne [x y field mod]
  (filter some?
    (for [m mod]
      (let [y2 (+ y (first m))
            x2 (+ x (second m))]
        (if (and (> x2 -1) (> y2 -1) (< x2 (count field)) (< y2 (count field)))
          [x2 y2 (nth (nth field y2) x2)]
          nil)))))

(defn newfield [field nes]
  (for [y (range 0 (count field))]
    (let [ne (filter #(= y (second %)) nes)
          row (nth field y)]
      (for [x (range 0 (count field))]
         (if (some #(= x (first %)) ne)
           (do (swap! flashes inc) (inc (nth row x)))
           (nth row x))))))

(defn flash [x y field done]
  ;(println "flash " x " " y " -- " done)
  (let [v (nth (nth field y) x)
        ky (keyword (str y))
        c (get done ky)
        c2 (if (empty? c) [] c)]
        ;(println "c " c " c2 " c2 " ky " ky)
    (if (and (> v 9) (not (some #(= x %) c)))
      (do (swap! flashes inc)
        (let [ne (getne x y field nex)
              f2 (newfield field ne)]
              ;(println "__ " (conj c2 x))
          [f2 (assoc done ky (conj c2 x))]))
      [field done])))

(defn resetf [old new]
  (if (empty? old)
    new
    (resetf (rest old) (conj new (if (> (first old) 9) 0 (first old))))))

(defn help1 [field done todo]
  (if (empty? todo)
    field
    (let [nxt (first todo)
          res (flash (first nxt) (second nxt) field done)]
      (help1 (first res) (second res) (rest todo)))))

(defn part1 [field runs]
  (if (= 0 runs)
    @flashes
    (let [field2 (for [row field] (map inc row))
          ;xx [[0 0 0] [0 0 0] [0 0 0]]
          looper (for [y (range 0 (count field)) x (range 0 (count field))] [x y])
          field3 (help1 field2 {} looper)
          field4 (for [row field3] (resetf row []))]
    ;(println field2)
    ;(println field3)
    ;(println field4)
    (do
    (println "##########################" runs)
    ;(doall (for [row field3] (println row)))
    (println "--------------------------" runs)
    (doall (for [row field4] (println row)))
    
    ;(println looper)
    ;(println (flash 0 0 field2 {}))
    ;(println (flash 1 1 field2 {}))
    ;(println "ff " flashes)
    ;(println (flash 1 1 field2 {:1 [1]}))
    ;(println "ff " flashes)
    ;(println (getne 0 9 field2 nex))
    ;(println (getne 9 0 field2 nex))
    ;(println (getne 1 9 field2 nex))
    ;(println (getne 9 1 field2 nex))
    ;(println (getne 1 1 field2 nex))
    ;(println (getne 0 0 xx nex))
    ;(println (newfield xx (getne 0 0 xx nex)))
       (part1 field4 (dec runs))))))

(defn part2 [lines]
  (help2 lines 0))

(defn run [filename]
  (let [lines (lib/lines-str filename)
        field (map #(clojure.string/split % #"") lines)
        field2 (for [row field] (map #(Integer/parseInt %) row))]
        ;(println lines)
        ;(println field)
        ;(println field2)

    (time (println "Part 1: " (part1 field2 2)))
    (time (println "Part 2: " (part2 lines)))))
