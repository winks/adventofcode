(ns aoc.lib
  (:require [clojure.string :as str]))

(defn lines-str [file]
  (str/split-lines (slurp file)))

(defn lines-int [file]
  (map (fn [x] (Integer/parseInt x)) (str/split-lines (slurp file))))

