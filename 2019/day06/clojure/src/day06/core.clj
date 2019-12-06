(ns day06.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.set :as cset])
  (:require [clojure.string :as str])
  (:gen-class))

(def cli-options
  [["-i" "--input FILE" "FILE"
    :default ""
    :validate [#(not (empty? %)) "Can't be empty"]]])

(defn f-lines [file]
  (str/split-lines (slurp file)))

(defn tuples [lst]
  (map #(str/split % #"\)") lst))

(defn app [s m]
  (let [p (str/split s #"\)")
        lx (first p)
        rx (second p)]
    (if (get-in m [rx])
      (do
        (println "y"))
;        (into m )
      (do
       (println "n" lx rx)
       (into m [[rx lx]])))))

(defn organize [lst]
  (println "##" lst (type lst) (count lst))
    (reduce into (map #(app % {}) lst)))

(defn isleaf? [k rd]
;(println "#isl " k (type k))
  (> 1 (count (filter #(= (str (second %)) k) rd))))

(defn walk [outer all acc]
;  (println "W " outer acc all)
  (if (= "COM" outer)
    (cons outer acc)
    (let [s (get-in all [(str outer)])]
;      (println "W2" outer (type outer) s)
      (cons outer (walk s all acc)))))

(defn counter [n v cs]
;(println "#" cs "::" n "::" v "::" )
(println "#" cs "::" (count n) "::" (count v) "::" )
;(println "#" (rest n) "::" (flatten (into [] (first n))) )
; v is not updated
  (if (empty? n)
    cs
    (let [sf (set (first n))
          nc (cset/difference sf (set v))]
      (counter (rest n) (flatten (into [] (first n))) (+ cs 1 (count sf) (count nc))))))


(defn -main [& args]
  (let [opt (:options (parse-opts args cli-options))
        lines (f-lines (:input opt))
        data (tuples lines)
        revdata (organize lines)
        leaves (map second (filter #(isleaf? (second %) revdata) data))
        paths (map reverse (map #(walk % revdata []) leaves))
        cnt (counter paths [] 0)
        st (first (first revdata))]
    (println "### " opt)
    ;(println "### " lines)
    (println "### " data)
    (println "###### ")
    (println "### " revdata)
    (println "###### ")
    (println "### " st)
    (println "### " leaves (count leaves))
    (println "### " paths)
    (println "###### ")
    (println "### num_paths" (count paths))
    (println "### orbits   " cnt)
    (println "")))
