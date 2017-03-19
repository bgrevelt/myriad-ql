package view.widgets

import java.text.SimpleDateFormat

import ast.NumericType
import com.typesafe.config.ConfigFactory
import values.{ NumericValue, UndefinedValue, Value }

import scala.util.{ Failure, Success, Try }
import scalafx.Includes._
import scalafx.scene.Node
import scalafx.scene.control.TextField

class NumericTextWidget(numberType: NumericType)(implicit val changeHandler: Value => Unit) extends QLWidget {

  private val textfield = new TextField()
  private val config = ConfigFactory.load()
  private val currencySymbol = config.getString("currencySymbol")

  textfield.onAction = handle {
    val rawValue = textfield.text.value.trim.stripPrefix(currencySymbol)
    val qlValue = Try(BigDecimal(rawValue)) match {
      case Success(parsedValue) => NumericValue.bigDecimalToNumericValue(parsedValue, numberType)
      case Failure(_) => UndefinedValue
    }

    this.setValue(qlValue)
    changeHandler(qlValue)
  }

  override def setValue(newVal: Value): Unit = newVal match {
    case n: NumericValue => textfield.text.value = NumericValue.upgradeNumericToType(n, numberType).toString
    case UndefinedValue => textfield.text.value = ""
    case other => sys.error(s"Incompatible value for numeric text field: $other")
  }

  override def getSFXNode: Node = textfield
}
