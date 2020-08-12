#include "bothsidestreelayoutproxy.h"
#include "utility/systemconfig.h"
#include "viewmodel/graphicsitem/connection.h"
#include "viewmodel/graphicsitem/node.h"
#include <QDebug>
#include <QRectF>

const QPointF OFFSET(10, 0);
const QPointF CUBIC_POINT(10, 0);

const QString BothSidesTreeLayoutProxy::NAME = "Both Sides";

BothSidesTreeLayoutProxy::BothSidesTreeLayoutProxy() : AbstractLayoutProxy() {
}

BothSidesTreeLayoutProxy::~BothSidesTreeLayoutProxy() {
}

void BothSidesTreeLayoutProxy::layout(Node* rootNode) {
  if (!rootNode) {
    return;
  }

  QList<Node*> leftHandSideNodes;
  QList<Node*> rightHandSideNodes;
  for (int i = 0; i < rootNode->childCount(); ++i) {
    if (0 == (i % 2)) {
      rightHandSideNodes << rootNode->childNodes()[i];
    } else {
      leftHandSideNodes << rootNode->childNodes()[i];
    }
  }

  const qreal xSpace = systemConfig(SystemConfig::bothSidesTreeLayoutNodeXSpace).toReal();
  const qreal ySpace = systemConfig(SystemConfig::bothSidesTreeLayoutNodeYSpace).toReal();
  qreal leftHandSideTotalHeight = -ySpace;
  qreal rightHandSideTotalHeight = -ySpace;

  foreach (Node* node, leftHandSideNodes) {
    leftHandSideTotalHeight += ySpace;
    const qreal childHeight = layoutChildFromRightToLeft(node);
    const qreal x = rootNode->boundingRect().left() - node->boundingRect().width() - xSpace;
    const qreal y = node->boundingRect().center().y() + childHeight / 2 + leftHandSideTotalHeight;
    node->setPos(x, y);
    drawConnectionRightToLeft(rootNode, node);
    leftHandSideTotalHeight += childHeight;
  }
  foreach (Node* node, rightHandSideNodes) {
    rightHandSideTotalHeight += ySpace;
    const qreal childHeight = layoutChildFromLeftToRight(node);
    const qreal x = rootNode->boundingRect().right() + xSpace;
    const qreal y = node->boundingRect().center().y() + childHeight / 2 + rightHandSideTotalHeight;
    node->setPos(x, y);
    drawConnectionLeftToRight(rootNode, node);
    rightHandSideTotalHeight += childHeight;
  }

  shiftRightToLeftNodes(leftHandSideNodes, 0, -rootNode->boundingRect().height() / 2 - leftHandSideTotalHeight / 2);
  shiftLeftToRightNodes(rightHandSideNodes, 0, -rootNode->boundingRect().height() / 2 - rightHandSideTotalHeight / 2);
}

QString BothSidesTreeLayoutProxy::name() const {
  return NAME;
}

qreal BothSidesTreeLayoutProxy::layoutChildFromLeftToRight(const Node* node) {
  const QRectF br = node->boundingRect();
  if (!node->hasChild()) {
    return br.height();
  }
  const qreal x = br.right() + systemConfig(SystemConfig::leftToRightTreeLayoutNodeXSpace).toReal();
  const qreal childHeight = childrenHeight(node);
  qreal y = br.center().y() - childHeight / 2;
  foreach (Node* childNode, node->childNodes()) {
    const qreal th = layoutChildFromLeftToRight(childNode);
    childNode->setPos(x, y + th / 2 - childNode->boundingRect().center().y());
    y += th + systemConfig(SystemConfig::leftToRightTreeLayoutNodeYSpace).toReal();
    drawConnectionLeftToRight(node, childNode);
  }
  return qMax(childHeight, br.height());
}

qreal BothSidesTreeLayoutProxy::layoutChildFromRightToLeft(const Node* node) {
  const QRectF br = node->boundingRect();
  if (!node->hasChild()) {
    return br.height();
  }
  const qreal x = br.left() - systemConfig(SystemConfig::leftToRightTreeLayoutNodeXSpace).toReal();
  const qreal childHeight = childrenHeight(node);
  qreal y = br.center().y() - childHeight / 2;
  foreach (Node* childNode, node->childNodes()) {
    const qreal th = layoutChildFromRightToLeft(childNode);
    const QRectF childBr = childNode->boundingRect();
    childNode->setPos(x - childBr.width(), y + th / 2 - childBr.center().y());
    y += th + systemConfig(SystemConfig::leftToRightTreeLayoutNodeYSpace).toReal();
    drawConnectionRightToLeft(node, childNode);
  }
  return qMax(childHeight, br.height());
}

qreal BothSidesTreeLayoutProxy::treeHeight(const Node* node) {
  return qMax(childrenHeight(node), node->boundingRect().height());
}

qreal BothSidesTreeLayoutProxy::childrenHeight(const Node* node) {
  if (!node->hasChild()) {
    return 0;
  }
  qreal leftToRightLayoutNodeYSpace = systemConfig(SystemConfig::leftToRightTreeLayoutNodeYSpace).toReal();
  qreal height = -leftToRightLayoutNodeYSpace;
  foreach (Node* childNode, node->childNodes()) {
    height += treeHeight(childNode);
    height += leftToRightLayoutNodeYSpace;
  }
  return height;
}

void BothSidesTreeLayoutProxy::drawConnectionLeftToRight(const Node* parentNode, const Node* childNode) {
  QPointF parentToChild = parentNode->scenePos() - childNode->scenePos();
  QPointF parentPos = parentToChild + parentNode->rightCenter() + OFFSET;
  QPointF childPos = childNode->leftCenter() - OFFSET;
  childNode->connection()->draw(parentPos, childPos, CUBIC_POINT);
}

void BothSidesTreeLayoutProxy::drawConnectionRightToLeft(const Node* parentNode, const Node* childNode) {
  QPointF parentToChild = parentNode->scenePos() - childNode->scenePos();
  QPointF parentPos = parentToChild + parentNode->leftCenter() - OFFSET;
  QPointF childPos = childNode->rightCenter() + OFFSET;
  childNode->connection()->draw(parentPos, childPos, -CUBIC_POINT);
}

void BothSidesTreeLayoutProxy::shiftRightToLeftNodes(QList<Node*> nodes, const qreal x, const qreal y) {
  foreach (Node* node, nodes) {
    QPointF p = node->pos();
    node->setPos(p + QPointF(x, y));
    drawConnectionRightToLeft(node->parentNode(), node);
  }
}

void BothSidesTreeLayoutProxy::shiftLeftToRightNodes(QList<Node*> nodes, const qreal x, const qreal y) {
  foreach (Node* node, nodes) {
    QPointF p = node->pos();
    node->setPos(p + QPointF(x, y));
    drawConnectionLeftToRight(node->parentNode(), node);
  }
}
