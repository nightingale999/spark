/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.spark.sql

import org.apache.avro.Schema

import org.apache.spark.annotation.Experimental

package object avro {
  /**
   * Adds a method, `avro`, to DataFrameWriter that allows you to write avro files using
   * the DataFileWriter
   */
  implicit class AvroDataFrameWriter[T](writer: DataFrameWriter[T]) {
    def avro: String => Unit = writer.format("avro").save
  }

  /**
   * Adds a method, `avro`, to DataFrameReader that allows you to read avro files using
   * the DataFileReader
   */
  implicit class AvroDataFrameReader(reader: DataFrameReader) {
    def avro: String => DataFrame = reader.format("avro").load

    @scala.annotation.varargs
    def avro(sources: String*): DataFrame = reader.format("avro").load(sources: _*)
  }

  /**
   * Converts a binary column of avro format into its corresponding catalyst value. The specified
   * schema must match the read data, otherwise the behavior is undefined: it may fail or return
   * arbitrary result.
   *
   * @param data the binary column.
   * @param jsonFormatSchema the avro schema in JSON string format.
   *
   * @since 2.4.0
   */
  @Experimental
  def from_avro(data: Column, jsonFormatSchema: String): Column = {
    new Column(AvroDataToCatalyst(data.expr, jsonFormatSchema))
  }

  /**
   * Converts a column into binary of avro format.
   *
   * @param data the data column.
   *
   * @since 2.4.0
   */
  @Experimental
  def to_avro(data: Column): Column = {
    new Column(CatalystDataToAvro(data.expr))
  }
}