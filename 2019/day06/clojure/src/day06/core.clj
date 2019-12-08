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
       (into m [[rx lx]])))

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

(defn counter [leaves revdata]
  (reduce + (map #(dec (count %)) (map #(walk (last %) revdata []) leaves))))

(defn -main [& args]
  (let [opt (:options (parse-opts args cli-options))
        lines (f-lines (:input opt))
        data (tuples lines)
        revdata (organize lines)
        leaves (map second (filter #(isleaf? (second %) revdata) data))
        paths (map reverse (map #(walk % revdata []) leaves))
        cnt (counter (keys revdata) revdata)
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
