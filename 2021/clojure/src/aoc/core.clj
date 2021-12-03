(ns aoc.core
  (:require [clojure.tools.cli :refer [parse-opts]])
  (:require [clojure.string :as str])
  (:require [aoc.day01 :as day01])
  (:require [aoc.day02 :as day02])
  (:require [aoc.day03 :as day03])
  (:gen-class))

(def cli-options
  [["-d" "--day DAY" "DAY"
    :default ""
    :validate [#(not (empty? %)) "Can't be empty"]]
  ["-f" "--file FILE" "FILE"
    :default ""]])


(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (let [opt (:options (parse-opts args cli-options))]
    (if (empty? (:day opt))
      (println "TBD: all")
      (let [filename (if (empty? (:file opt)) (str "../input/day" (:day opt) "/input.txt") (:file opt))
            fun (resolve (symbol (str "aoc.day" (:day opt) "/run")))]
            (println (str "####" fun))
            (time (fun filename))))))
